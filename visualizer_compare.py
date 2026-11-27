
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider
from pathlib import Path


# --------------------------------------------------
# Load simulation
# --------------------------------------------------

def load_simulation(filename):
    metadata = {}
    simulations = []

    with open(filename, "r") as file:
        lines = file.readlines()

    reading_data = False
    current_matrix = []

    for line in lines:
        line = line.strip()

        if line == "[DATA]":
            reading_data = True
            continue

        if not reading_data:
            if "," in line and line != "[METADATA]":
                key, value = line.split(",", 1)
                metadata[key] = float(value)
            continue

        if line.startswith("iteration"):
            if current_matrix:
                simulations.append(np.array(current_matrix))
                current_matrix = []
            continue

        if line:
            row = [float(value) for value in line.split(",")]
            current_matrix.append(row)

    if current_matrix:
        simulations.append(np.array(current_matrix))

    return metadata, simulations


# --------------------------------------------------
# Calculate average temperature
# --------------------------------------------------

def calculate_averages(metadata, simulations):
    averages = []

    source_row = int(metadata["sourceRow"])
    source_col = int(metadata["sourceCol"])

    for matrix in simulations:
        total = np.sum(matrix) - matrix[source_row, source_col]
        average = total / (matrix.size - 1)
        averages.append(average)

    return averages


# --------------------------------------------------
# Load all materials
# --------------------------------------------------

directory = Path(__file__).parent / "simulations"
files = sorted(directory.glob("*.csv"))

if not files:
    raise SystemExit("No simulation files found.")

materials = []

for filename in files:
    metadata, simulations = load_simulation(filename)

    averages = calculate_averages(metadata, simulations)

    materials.append({
        "name": filename.stem.capitalize(),
        "alpha": metadata["alpha"],
        "dt": metadata["dt"],
        "T0": metadata["T0"],
        "averages": averages
    })


# --------------------------------------------------
# General configuration
# --------------------------------------------------

total_frames = max(
    len(material["averages"])
    for material in materials
)

interval = min(
    material["dt"]
    for material in materials
) * 1000

for material in materials:
    material["temperatures"] = (
        [material["T0"]] + material["averages"]
    )

all_temperatures = [
    temperature
    for material in materials
    for temperature in material["temperatures"]
]

global_min = min(all_temperatures)
global_max = max(all_temperatures)

padding = max((global_max - global_min) * 0.1, 1)

max_time = max(
    len(material["temperatures"]) * material["dt"]
    for material in materials
)


# --------------------------------------------------
# Create figure
# --------------------------------------------------

fig, (line_ax, bar_ax) = plt.subplots(
    1, 2,
    figsize=(15, 7)
)

fig.subplots_adjust(
    bottom=0.25,
    top=0.88,
    wspace=0.3
)

fig.suptitle(
    "Thermal Simulation Comparison",
    fontsize=15
)


# --------------------------------------------------
# Line chart
# --------------------------------------------------

lines = []

for material in materials:

    line, = line_ax.plot(
        [],
        [],
        linewidth=2,
        marker="o",
        markersize=4,
        label=(
            f"{material['name']} "
            f"(α={material['alpha']:.3e})"
        )
    )

    lines.append(line)

line_ax.set_title("Average Temperature Evolution")
line_ax.set_xlabel("Time (s)")
line_ax.set_ylabel("Temperature (°C)")

line_ax.set_xlim(0, max_time)

line_ax.set_ylim(
    global_min - padding,
    global_max + padding
)

line_ax.grid(True, alpha=0.3)


# --------------------------------------------------
# Derivative labels at line tips
# --------------------------------------------------

derivative_labels = []

for line in lines:

    label = line_ax.annotate(
        "",
        xy=(0, 0),
        xytext=(8, 8),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold"
    )

    label.set_color(line.get_color())
    derivative_labels.append(label)


# --------------------------------------------------
# Bar chart
# --------------------------------------------------

names = [
    material["name"]
    for material in materials
]

initial_values = [
    material["T0"]
    for material in materials
]

bar_container = bar_ax.bar(
    names,
    initial_values
)

bar_patches = list(bar_container)


# Temperature labels inside bars

bar_labels = []

for bar in bar_patches:

    label = bar_ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        "",
        ha="center",
        va="top",
        color="white",
        fontweight="bold"
    )

    bar_labels.append(label)


bar_ax.set_title("Current Average Temperature")
bar_ax.set_ylabel("Temperature (°C)")

bar_ax.set_ylim(
    global_min - padding,
    global_max + padding
)

bar_ax.grid(axis="y", alpha=0.3)


# --------------------------------------------------
# Legend
# --------------------------------------------------

legend = line_ax.legend(loc="best")


# --------------------------------------------------
# Animation state
# --------------------------------------------------

current_frame = 0
playing = False


# --------------------------------------------------
# Update visualization
# --------------------------------------------------

def update(frame):
    global current_frame

    current_frame = int(frame)

    for index, material in enumerate(materials):

        temperatures = material["temperatures"]

        material_frame = min(
            current_frame,
            len(material["averages"])
        )

        dt = material["dt"]

        times = np.arange(len(temperatures)) * dt

        # Update line and points
        lines[index].set_data(
            times[:material_frame + 1],
            temperatures[:material_frame + 1]
        )

        # Update bar and temperature label
        temperature = temperatures[material_frame]

        bar_patches[index].set_height(temperature)

        bar_labels[index].set_position((
            bar_patches[index].get_x() + bar_patches[index].get_width() / 2,
            temperature - padding * 0.1
        ))

        bar_labels[index].set_text(f"{temperature:.2f} °C")

        # Calculate derivative
        if material_frame == 0 or dt == 0:

            derivative_text = "dT/dt = --"

        else:

            previous_temperature = temperatures[material_frame - 1]
            current_temperature = temperatures[material_frame]

            derivative = (
                current_temperature - previous_temperature
            ) / dt

            derivative_text = f"{derivative:+.2f} °C/s"

        # Position derivative at line tip
        tip_time = times[material_frame]
        tip_temperature = temperatures[material_frame]

        derivative_labels[index].xy = (
            tip_time,
            tip_temperature
        )

        derivative_labels[index].set_text(
            derivative_text
        )

    # Update information
    time = current_frame * materials[0]["dt"]

    fig.suptitle(
        f"Thermal Simulation Comparison | "
        f"Iteration: {current_frame}/{total_frames} | "
        f"Time: {time:.2f} s",
        fontsize=14
    )

    # Synchronize slider
    slider.eventson = False
    slider.set_val(current_frame)
    slider.eventson = True

    return lines + bar_patches + derivative_labels + bar_labels


# --------------------------------------------------
# Animation
# --------------------------------------------------

def animate(frame=None):
    global current_frame, playing

    if not playing:
        return lines + bar_patches + derivative_labels + bar_labels

    if current_frame >= total_frames:
        playing = False
        play_button.label.set_text("Play")
        ani.event_source.stop()
        fig.canvas.draw_idle()

        return lines + bar_patches + derivative_labels + bar_labels

    update(current_frame + 1)

    if current_frame >= total_frames:
        playing = False
        play_button.label.set_text("Play")
        ani.event_source.stop()

    return lines + bar_patches + derivative_labels + bar_labels


# --------------------------------------------------
# Play / Pause
# --------------------------------------------------

def toggle_animation(event):
    global playing

    if playing:

        # Pause
        playing = False
        ani.event_source.stop()
        play_button.label.set_text("Play")

    else:

        # Restart if animation reached the end
        if current_frame >= total_frames:
            update(0)

        # Start playback
        playing = True
        play_button.label.set_text("Pause")

        ani.event_source.start()

    fig.canvas.draw_idle()

# --------------------------------------------------
# Reset
# --------------------------------------------------

def reset_animation(event):
    global playing

    playing = False

    ani.event_source.stop()

    update(0)

    play_button.label.set_text("Play")

    fig.canvas.draw_idle()

# --------------------------------------------------
# Slider
# --------------------------------------------------

def slider_update(value):

    if not playing:
        update(int(value))
        fig.canvas.draw_idle()


# --------------------------------------------------
# Controls
# --------------------------------------------------

button_ax = fig.add_axes(
    [0.15, 0.12, 0.14, 0.05]
)

play_button = Button(
    button_ax,
    "Play"
)

play_button.on_clicked(toggle_animation)


slider_ax = fig.add_axes(
    [0.15, 0.055, 0.70, 0.025]
)

slider = Slider(
    slider_ax,
    "Iteration",
    0,
    total_frames,
    valinit=0,
    valstep=1
)

slider.on_changed(slider_update)


reset_button_ax = fig.add_axes(
    [0.75, 0.12, 0.14, 0.05]
)

reset_button = Button(
    reset_button_ax,
    "Reset"
)

reset_button.on_clicked(reset_animation)


# --------------------------------------------------
# Start
# --------------------------------------------------

ani = FuncAnimation(
    fig,
    animate,
    interval=interval,
    repeat=False,
    blit=False,
    cache_frame_data=False
)

# Start paused at iteration zero
ani.event_source.stop()

update(0)

fig.canvas.draw()

plt.show()
