
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider

from pathlib import Path
import math


# --------------------------------------------------
# CARGAR SIMULACIONES
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


# Buscar todos los archivos CSV
directory = Path(__file__).parent / "simulations"
files = sorted(directory.glob("*.csv"))

if not files:
    raise FileNotFoundError(
        "No se encontraron archivos CSV en el directorio simulations."
    )


# Cargar todos los materiales
materials = []

for filename in files:
    metadata, simulations = load_simulation(filename)

    if not simulations:
        print(f"Advertencia: {filename.name} no contiene datos.")
        continue

    source_row = int(metadata["sourceRow"])
    source_col = int(metadata["sourceCol"])

    # Calcular promedio sin contar la fuente
    averages = []

    for matrix in simulations:
        total = np.sum(matrix) - matrix[source_row, source_col]
        average = total / (matrix.size - 1)
        averages.append(average)

    materials.append({
        "name": filename.stem.capitalize(),
        "metadata": metadata,
        "simulations": simulations,
        "averages": averages
    })


if not materials:
    raise ValueError("No hay simulaciones válidas para visualizar.")


# --------------------------------------------------
# CONFIGURACIÓN GENERAL
# --------------------------------------------------

total_frames = max(
    len(material["simulations"]) for material in materials
)

current_frame = 0
playing = False

# Escala de temperatura compartida
global_min = min(
    np.min(matrix)
    for material in materials
    for matrix in material["simulations"]
)

global_max = max(
    np.max(matrix)
    for material in materials
    for matrix in material["simulations"]
)

# Distribución de las placas
num_materials = len(materials)

columns = math.ceil(math.sqrt(num_materials))
rows = math.ceil(num_materials / columns)

fig, axes = plt.subplots(
    rows,
    columns,
    figsize=(8 * columns, 7 * rows + 2),
    squeeze=False
)

axes = axes.flatten()


# --------------------------------------------------
# DISTRIBUCIÓN DEL ESPACIO
# --------------------------------------------------

plt.subplots_adjust(
    left=0.09,
    right=0.87,
    bottom=0.30,
    top=0.88,
    hspace=0.95,
    wspace=0.01
)

images = []
infos = []


# --------------------------------------------------
# CREAR PLACAS
# --------------------------------------------------

for index, material in enumerate(materials):

    ax = axes[index]

    metadata = material["metadata"]
    matrix = material["simulations"][0]

    dx = metadata["dx"]
    dy = metadata["dy"]

    height = matrix.shape[0] * dy
    width = matrix.shape[1] * dx

    image = ax.imshow(
        matrix,
        cmap="coolwarm",
        interpolation="bicubic",
        origin="upper",
        extent=[0, width, height, 0],
        aspect="equal",
        vmin=global_min,
        vmax=global_max
    )

    images.append(image)

    ax.set_xlabel("X (m)", labelpad=8)
    ax.set_ylabel("Y (m)", labelpad=8)

    ax.set_title(
        material["name"],
        pad=12,
        fontsize=12,
        fontweight="bold"
    )

    # Información debajo de cada placa
    info = ax.text(
        0.5,
        -0.32,
        "",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=8.5,
        linespacing=1.5
    )

    infos.append(info)


# Ocultar espacios vacíos
for index in range(num_materials, len(axes)):
    axes[index].set_visible(False)


# --------------------------------------------------
# BARRA DE COLOR
# --------------------------------------------------

# Crear un espacio independiente para el gradiente
cax = fig.add_axes([0.91, 0.32, 0.018, 0.54])

colorbar = fig.colorbar(
    images[0],
    cax=cax
)

colorbar.set_label(
    "Temperature (°C)",
    labelpad=10
)


# --------------------------------------------------
# TÍTULO GENERAL
# --------------------------------------------------

fig.suptitle(
    "Heat Diffusion - Material Comparison",
    fontsize=16,
    fontweight="bold",
    y=0.96
)


# --------------------------------------------------
# ACTUALIZAR PLACAS
# --------------------------------------------------

def update(frame):
    global current_frame

    current_frame = frame

    for index, material in enumerate(materials):

        metadata = material["metadata"]
        simulations = material["simulations"]

        # Mantener el último estado si una simulación termina antes
        material_frame = min(
            current_frame,
            len(simulations) - 1
        )

        matrix = simulations[material_frame]

        images[index].set_data(matrix)

        time = material_frame * metadata["dt"]
        average = material["averages"][material_frame]

        # Información dividida para evitar solapamientos
        infos[index].set_text(
            f"Iteration: {material_frame + 1}/{len(simulations)}"
            f" | Time: {time:.2f} s\n"
            f"Average: {average:.2f} °C"
            f" | Alpha: {metadata['alpha']:.3e}\n"
            f"Initial: {metadata['T0']:.2f} °C"
            f" | Source: {metadata['Th']:.2f} °C"
        )

    slider.eventson = False
    slider.set_val(current_frame)
    slider.eventson = True

    fig.canvas.draw_idle()


# --------------------------------------------------
# ANIMACIÓN
# --------------------------------------------------

def animate(frame):
    global current_frame

    if playing:

        next_frame = current_frame + 1

        if next_frame >= total_frames:
            next_frame = 0

        update(next_frame)

    return images


# --------------------------------------------------
# CONTROLES
# --------------------------------------------------

# Botón Play / Pause
ax_play = fig.add_axes([0.15, 0.10, 0.14, 0.05])
btn_play = Button(ax_play, "Play")

# Botón Reset
ax_reset = plt.axes([0.75, 0.10, 0.14, 0.05])
btn_reset = Button(ax_reset, "Reset")


# Barra de progreso
ax_slider = fig.add_axes([0.15, 0.055, 0.70, 0.025])

slider = Slider(
    ax_slider,
    "Iteration",
    0,
    total_frames - 1,
    valinit=0,
    valstep=1
)


def play_pause(event):
    global playing

    playing = not playing

    if playing:

        if current_frame >= total_frames - 1:
            update(0)

        btn_play.label.set_text("Pause")
        ani.event_source.start()

    else:

        btn_play.label.set_text("Play")
        ani.event_source.stop()

def reset_animation(event):
    global playing

    playing = False
    ani.event_source.stop()

    update(0)

    btn_play.label.set_text("Play")

    fig.canvas.draw_idle()

def slider_changed(value):
    global playing

    playing = False

    btn_play.label.set_text("Play")

    update(int(value))


btn_play.on_clicked(play_pause)
btn_reset.on_clicked(reset_animation)
slider.on_changed(slider_changed)


# --------------------------------------------------
# INICIAR ANIMACIÓN
# --------------------------------------------------

interval = materials[0]["metadata"]["dt"] * 1000

ani = FuncAnimation(
    fig,
    animate,
    interval=interval,
    repeat=False,
    cache_frame_data=False
)

ani.event_source.stop()

update(0)

plt.show()
