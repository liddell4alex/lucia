# Lucia 

## Modeling heat transfer in a metal plate

## Author
**Name:** Alejandro Cons Andablo

**Affiliation:** Universidad Nacional Autónoma de México (UNAM)

**Contact:** alexmixsep@gmail.com <br>

## Objective
The objective of this project is to model and simulate an adiabatic heat transfer system without a dissipation coefficient in a metal plate over time. The palte will be represented as a matrix with cells.

The metal plate will have an initial temperature. An initial point of heat source will begin to warm the plate, and we will observe how the heat is distribuited throughout the plate.

I will use the physical phenomenon known as thermal conduction.

## Model
**Static conditions:**
- Rectangular plate with variable dimensions.
- Represented on a 2D grid.
- $\Delta x = \Delta y = 0.01$ m equivalent to 1.0 cm
- Isolated edges— meaning heat cannot escape.
    - Using ghost cells around the edge, which always have the same temperature as those at the edge.

**Initial conditions:**
- $Dims = (L_x, L_y)$: Plate dimensions.
- $T_0$: Initial plate temperature. 
- $T_h$: Heat source temperature.
- $P = (x_h, y_h)$: Heat source starting cell.
- $\alpha$: Thermal diffusivity of a metal (example: silver = 113e-6)

## Matematical issues
I will use the two-dimensional heat equation:

$$
\frac{\partial T}{\partial t} = \alpha\left(\frac{\partial^2T}{\partial x^2} + \frac{\partial^2T}{\partial y^2}\right)
$$

Where:
- $\frac{\partial T}{\partial t}$: Change in temperature over time.
- $\frac{\partial^2T}{\partial x^2}$: Spatial variation of temperature in x.
- $\frac{\partial^2T}{\partial y^2}$: Spatial variation of temperature in y.
- $\alpha$: Thermal diffusivity

Understanding **thermal diffusivity**.

$$
\alpha = \frac{k}{\text{ρ} c_p}
$$

It indicates how quickly a temperature variation spreads through a material.
- $k$: Thermal conductivity.
- $\text{ρ}$: Material density.
- $c_p$: Specific heat capacity.

Is necessary to discretize the space. For this, the space is divided into points separated by a constant distance: $\Delta x$ horizontally and $\Delta y$ vertically. The temperature will be measured at these points on the plate, which will initially all be at a uniform temperature.

The above is represented by a matrix, where each cell is a point with a temperature.

$$
\begin{bmatrix}
T_{11} & T_{12} & \cdots & T_{1n} \\
T_{21} & T_{22} & \cdots & T_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
T_{m1} & T_{m2} & \cdots & T_{mn} \\
\end{bmatrix}
$$

In this way, we work with discrete points. For a cell $T_{i,j}$, it has 4 neighbors:

$$
\begin{matrix}
          & T_{i-1,j} &           \\
T_{i,j-1} &  T_{i,j}  & T_{i,j+1} \\
          & T_{i+1,j} &           \\
\end{matrix}
$$

Now, to simulate the temperature distribution on the plate, it is necessary to know how the temperature at each point changes relative to its neighbors. To do this, we use spatial derivatives, which we approximate using finite differences. Spatial derivatives allow us to determine how temperatures change as we move through space.

To aproximate the value of a function at a $a$, using its derivatives evaluated at a reference point $x$, we use Taylor series:

$$
f(x) \approx \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}(x-a)^n
$$

Using the expansion of Taylor series we aproximate the value of a function at a nearby point using the derivatives at the original point. We want to expand the function T(x) horizontally. The expansion to the right is done using $x + \Delta x$ and the expansion to the left is done using $x - \Delta x$

$$
T(x + \Delta x) \approx T(x) + \frac{\partial T(x)}{\partial x}\Delta x + \frac{1}{2!}\frac{\partial ^{2}T(x)}{\partial ^2x}{\Delta x}^2 + \frac{1}{3!} \frac{\partial ^3T(x)}{\partial ^3x}{\Delta x}^3 + \cdots 
$$

<br>

$$
T(x - \Delta x) \approx T(x) - \frac{\partial T(x)}{\partial x}\Delta x + \frac{1}{2!}\frac{\partial ^{2}T(x)}{\partial ^2x}{\Delta x}^2 - \frac{1}{3!} \frac{\partial ^3T(x)}{\partial ^3x}{\Delta x}^3 + \cdots 
$$

And then we add the expresions and simplifying the expression down to the second-order derivative, since that is what is needed for the heat equation:

$$
T(x + \Delta x) + T(x - \Delta x) \approx 2T(x) + \cancel{\frac{\partial T(x)}{\partial x}\Delta x - \frac{\partial T(x)}{\partial x}\Delta x} + 2\frac{1}{2!}\frac{\partial ^{2}T(x)}{\partial ^2x}{\Delta x}^2
$$

<br>

$$
T(x + \Delta x) + T(x - \Delta x) \approx 2T(x) + \frac{\partial ^{2}T(x)}{\partial ^2x}{\Delta x}^2
$$

<br>

$$
T(x + \Delta x) - 2T(x) + T(x - \Delta x) \approx \frac{\partial ^{2}T(x)}{\partial ^2x}{\Delta x}^2
$$

<br>

$$
\boxed{
\frac{T(x + \Delta x) - 2T(x) + T(x - \Delta x)}{ {\Delta x}^2 } \approx \frac{\partial ^{2}T(x)}{\partial ^2x}
}
$$

To expand T(x) vertically is the same but with $y$. The upward expansion is done using $y + \Delta y$ and the downward expansion is done using $y - \Delta y$

$$
T(y + \Delta y) \approx T(y) + \frac{\partial T(y)}{\partial y}\Delta y + \frac{1}{2!}\frac{\partial ^{2}T(y)}{\partial ^2y}{\Delta y}^2 + \frac{1}{3!} \frac{\partial ^3T(y)}{\partial ^3y}{\Delta y}^3 + \cdots 
$$

<br>

$$
T(y - \Delta y) \approx T(y) - \frac{\partial T(y)}{\partial y}\Delta y + \frac{1}{2!}\frac{\partial ^{2}T(y)}{\partial ^2y}{\Delta y}^2 - \frac{1}{3!} \frac{\partial ^3T(y)}{\partial ^3y}{\Delta y}^3 + \cdots 
$$

The same as before, add the expansions and take up to the second-order derivative:

$$
T(y + \Delta y) + T(y - \Delta y) \approx 2T(y) + \cancel{\frac{\partial T(y)}{\partial y}\Delta y - \frac{\partial T(y)}{\partial y}\Delta y} + 2\frac{1}{2!}\frac{\partial ^{2}T(y)}{\partial ^2y}{\Delta y}^2
$$

<br>

$$
T(y + \Delta y) + T(y - \Delta y) \approx 2T(y) + \frac{\partial ^{2}T(y)}{\partial ^2y}{\Delta y}^2
$$

<br>

$$
T(y + \Delta y) - 2T(y) + T(y - \Delta y) \approx \frac{\partial ^{2}T(y)}{\partial ^2y}{\Delta y}^2
$$

<br>

$$
\boxed{
\frac{T(y + \Delta y) - 2T(y) + T(y - \Delta y)}{ {\Delta y}^2 } \approx \frac{\partial ^{2}T(y)}{\partial ^2y}
}
$$

From now on, the following elements will be replaced in order to work according to the matrix:

$$
T(x,y) = T_{i,j}
$$

At $x$:

$$
T(x + \Delta x) = T_{i,j+1}
$$
$$
T(x - \Delta x) = T_{i,j-1}
$$

At $y$:

$$
T(y + \Delta y) = T_{i+1,j}
$$

$$
T(y - \Delta y) = T_{i-1,j}
$$

Using this procedure, we have discretized the spatial derivatives of temperature, allowing us to numerically calculate their variations in the horizontal and vertical directions. And we can continue:


When the heat is applied, the temperature at various cells will change. The change in temperature at the cells within the matrix $\left(\frac{\partial T_{i,j}}{\partial t}\right)$ will be aproximated with:

$$
\frac{\partial ^2T_{i,j}}{\partial x^2} \approx \frac{T_{i,j+1} - 2T_{i,j} + T_{i,j-1}}{\Delta x^2}
$$

And: 

$$
\frac{\partial ^2T_{i,j}}{\partial y^2} \approx \frac{T_{i+1,j} - 2T_{i,j} + T_{i-1,j}}{\Delta y^2}
$$

Then substituting both approximations into the heat equation:

$$
\frac{\partial T_{i,j}}{\partial t} = \alpha\left[\frac{T_{i,j+1} - 2T_{i,j} + T_{i,j-1}}{\Delta x^2}  + \frac{T_{i+1,j} - 2T_{i,j} + T_{i-1,j}}{\Delta y^2}\right]
$$

The temperature changes over time, and the heat differential equation contains a derivative whith respect to time. This means that it is necessary to measure the change over time. The explicit Euler method will be used to aproximate the change in time.

Taking into account:

$$
\frac{y_{n+1} - y_{n}}{\Delta t} = f(t, y)
$$

We can replace the heat equation with the formal definition of the derivative:

$$
\frac{dx}{dy} = \lim_{h \to 0} \frac{f(x + h) - f(x)}{h}
$$

$$
\frac{\partial T_{i,j}}{\partial t} \approx \frac{T^{n+1}_{i,j} - T^{n}_{i,j}}{\Delta t}
$$

It is an approximation because computers cannot calculate infinitely small time changes.

Substituting:

$$
\frac{T^{n+1}_{i,j} - T^{n}_{i,j}}{\Delta t} \approx \alpha\left[\frac{T^{n}_{i,j+1} - 2T^{n}_{i,j} + T^{n}_{i,j-1}}{\Delta x^2}  + \frac{T^{n}_{i+1,j} - 2T^{n}_{i,j} + T^{n}_{i-1,j}}{\Delta y^2}\right]
$$

Solving for the approximate temperature at n+1:

$$
T^{n+1}_{i,j} \approx T^{n}_{i,j} + \Delta t \ \alpha\left[\frac{T^{n}_{i,j+1} - 2T^{n}_{i,j} + T^{n}_{i,j-1}}{\Delta x^2}  + \frac{T^{n}_{i+1,j} - 2T^{n}_{i,j} + T^{n}_{i-1,j}}{\Delta y^2}\right]
$$

This will be the equation used to measure the temperature change in each cell of the matrix.

It is necessary to establish the behavior of the isolated edges. Ghost cells will be used represented as:

$$
T_{-1} = T_{0}
$$

In other words, the temperature of the preceding cell and that of the edge are equal. This leads to the following in the heat equation. Originally with $T_{-1}$ and $T_{0}$, it is:

$$
\left[\frac{T_{i,1} - 2T_{i,0} + T_{i,-1}}{\Delta x^2}\right] \ \text{and} \ \left[\frac{T_{1,j} - 2T_{0,j} + T_{-1,j}}{\Delta y^2}\right]
$$

But because we have $T_{-1} = T_{0}$ it turns into:

$$
\left[\frac{T_{i,1} - T_{i,0}}{\Delta x^2}\right] \ \text{and} \ \left[\frac{T_{1,j} - T_{0,j}}{\Delta y^2}\right]
$$

About the permanent heat source, it will be defined as:

Given a cell $(x_h, y_h)$

$$
T_{i,j} = T_h
$$

If $T_h = 100$ C°, that value will be permanent.

## Use

First to clone and compile:

```
git clone https://github.com/liddell4alex/lucia.git
cd lucia
mkdir -p simulations
make
```

Then the executable will be in the `build/` directory. To run it use `./build/lucia ...`. If executed from within the `build` directory or another, it will result in an error because the `simulations` directory is not located there; furthermore, even if a `simulations` directory were created in that location, the visualizers look for it in the project's root folder.

```
./build/lucia help
```

To show the usage of the program:

```
Uso: lucia <metal> <alpha> <puntos x> <puntos y> <T0> <Th> <hx> <hy> <iter>
Donde:
    - <metal> ====> Nombre del metal con el que se va a trabajar (minusculas)
    - <alpha> ====> Difusividad térmica del material en m²/s.
    - <puntos x> => Cantidad de puntos en x de la placa.
    - <puntos y> => Cantidad de puntos en y de la placa.
    - <T0> =======> Temperatura inicial de la placa en °C.
    - <Th> =======> Temperatura de la fuente en °C.
    - <hx> =======> Punto de aplicación de la fuente en la placa en °C.
    - <hy> =======> Punto de aplicación de la fuente en la placa en °C.
    - <iter> =====> Número de iteraciones.

La cantidad de puntos en x y y también influye en las dimensiones de la placa, la distancia entre cada punto vertical y horizontalmente es 0.01 metros. Si se determina que en x hay 100 puntos la placa medirá 1.0 metros de ancho.
                        
Ejemplo: lucia silver 149e-6 5 5 25.0 200.0 0 3 200
```
As the help section states, to use it you must provide the 9 specified arguments, which serve as the initial conditions for the simulation.

The following image shows the thermal diffusivity of some metals:

<div align="center">
  <img src="https://www.nuclear-power.com/wp-content/uploads/2017/10/thermal-diffusivity-of-various-materials.png" alt="Thermal diffusivity of some metals" width="300">
  <p>
    <em>Source: <a href="https://www.nuclear-power.com/nuclear-engineering/heat-transfer/thermal-conduction/heat-conduction-equation/thermal-diffusivity/">www.nuclear-power.com</a></em>
  </p>
</div>

There are a few things to keep in mind:

- The directory `simulations` is needed to save the csv output files for the visualizer. The output files are stored as follows: `<metal>.csv`.
- The first argument specifies the name of the file where the results of this simulation will be saved. If you run two simulations using the same name, any existing file with that name will be overwritten by the new results.
- Thermal diffusivity must be entered in units of m²/s.
- The distance between each point is 0.01 meters. This means that if we specify 10 points along the x-axis, the plate will have a width of 0.1 meters—that is, 10 cm.
- The temperature source point is a coordinate within the set of points; that is, the values ​​assigned cannot exceed the total number of points available for each axis.
- The change in time is 0.1 seconds, so if we specify 10 iterations, the simulation will represent the passage of 1 second in time.
- The source can be at a negative temperature.

## Examples of usage and visualization of results

First testing with a silver plate:

```
./build/lucia silver 149e-6 5 5 25.0 200.0 0 3 200
```

When the execution finishes, the results will be saved in the `silver.csv` file in the `simulations` directory.

There are two visualizers for displaying the results: one shows heat transfer between points on the plate, and it runs as follows:

```
python visualizer_plates.py
```

And it shows

<div align="center">
  <img src="https://i.imgur.com/KIId6f7.gif" alt="Visualizing the spread of heat through the silver plate over time" width="500">
</div>
<br>

The other visualizer is used to observe changes in the plate's average temperature over time in two ways: one graph shows the relationship between temperature and time, while the other graph illustrates how the plate's average temperature increases. It runs as follos:

```
python visualizer_compare.py
```

And it shows

<div align="center">
  <img src="https://i.imgur.com/XXIfcCY.gif" alt="Visualizing the change in average temperature over time" width="500">
</div>
<br>

From now on, the visualizations will be displayed without showing the execution command, as it is exactly the same.

This is where it gets interesting: we can run the simulation for various metals—ideally with the same specifications for the plate—and compare the changes over time. For example, for silver, gold, aluminum, and iron:

```
./build/lucia silver 149e-6 5 5 25.0 200.0 0 3 200
./build/lucia gold 127e-6 5 5 25.0 200.0 0 3 200
./build/lucia aluminum 97.5e-6 5 5 25.0 200.0 0 3 200
./build/lucia iron 22.8e-6 5 5 25.0 200.0 0 3 200
```

And with the visualizers we can get:

<p align="center">
  <img src="https://i.imgur.com/Hy5sjYH.gif" width="350">
  <img src="https://i.imgur.com/WEEzX6u.gif" width="350">
</p>

