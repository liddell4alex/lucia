# Lucia 

## Modeling heat transfer in a metal plate

## Author
**Name:** Alejandro Cons Andable

**Affiliation:** Universidad Nacional Autónoma de México (UNAM)

**Contact:** alexmixsep@gmail.com <br>

## Objective
The objective of this project is to model and simulate the propagation of heat in a metal plate over time. The palte will be represented as a matrix with cells.

The metal plate will have an initial temperature. An initial point of heat source will begin to warm the plate, and we will observe how the heat is distribuited throughout the plate.

I will use the physical phenomenon known as thermal conduction.

## Model
**Static conditions:**
- Rectangular plate of variable dimensions.
- Plate made of aluminum.
- Specific heat capacity.
- Using thermal conduction.
- Represented on a 2D grid.
- Isolated edges— meaning heat cannot escape.
    - Using ghost cells around the edge, which always have the same temperature as those at the edge.

**Initial conditions:**
- $Dims = (L_x, L_y)$: Plate dimensions.
- $T_0$: Initial plate temperature. 
- $T_h$: Heat source temperature.
- $P = (x_h, y_h)$: Heat source starting cell.

## Matematical issues
I will use the two-dimensional heat equation:

$$
\frac{\partial T}{\partial t} = \alpha\left(\frac{\partial^2T}{\partial x^2} + \frac{\partial^2T}{\partial y^2}\right)
$$

Where:
- $\frac{\partial T}{\partial t}$: Change in temperature over time.
- $\frac{\partial^2T}{\partial x^2}$: Spatial variation of temperature in x.
- $\frac{\partial^2T}{\partial y^2}$: Spatial variation of temperature in y.
- $\alpha$: Thermal diffusiviy

Understanding **thermal diffusivity**.

$$
\alpha = \frac{k}{\rho\,c_p}
$$

It indicates how quickly a temperature variation spreads through a material.
- $k$: Thermal conductivity.
- $\rho$: Material density.
- $c_p$: Specific heat capacity (Of the aluminum in this case).

## Model
The plate will be represented as a matrix of cells with values corresponding to temperatures, which will initially be uniform across the entire plate.

$$
\begin{bmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn} \\
\end{bmatrix}
$$

When the heat is applied, the temperature at various cells will change. The change in temperature at the cells within the matrix $\left(\frac{\partial T_{i,j}}{\partial t}\right)$ will be aproximated with:

$$
\frac{\partial ^2T}{\partial x^2} \approx \frac{T_{i+1,j} - 2T_{i,j} + T_{i-1,j}}{\Delta x^2}
$$

And: 

$$
\frac{\partial ^2T}{\partial y^2} \approx \frac{T_{i,j+1} - 2T_{i,j} + T_{i,j-1}}{\Delta y^2}
$$

Then substituting both approximations into the heat equation:

$$
\frac{\partial T_{i,j}}{\partial t} = \alpha\left[\frac{T_{i+1,j} - 2T_{i,j} + T_{i-1,j}}{\Delta x^2}  + \frac{T_{i,j+1} - 2T_{i,j} + T_{i,j-1}}{\Delta y^2}\right]
$$

The temperature changes over time, and the heat differential equation contains a derivative whith respect to time. This means that it is necessary to measure the change over time. The explicit Euler method will be used to aproximate the change in time.

Taking into account:

$$
\frac{y_{n+1} - y_{n}}{\Delta t} = f(t, y)
$$

We can modify the heat equation:

$$
\frac{\partial T_{i,j}}{\partial t} \approx \frac{T^{n+1}_{i,j} - T^{n}_{i,j}}{\Delta t}
$$

Substituting:

$$
\frac{T^{n+1}_{i,j} - T^{n}_{i,j}}{\Delta t} \approx \alpha\left[\frac{T^{n}_{i+1,j} - 2T^{n}_{i,j} + T^{n}_{i-1,j}}{\Delta x^2}  + \frac{T^{n}_{i,j+1} - 2T^{n}_{i,j} + T^{n}_{i,j-1}}{\Delta y^2}\right]
$$

Solving for the approximate temperature at n+1:

$$
T^{n+1}_{i,j} \approx T^{n}_{i,j} + \Delta t\,\alpha\left[\frac{T^{n}_{i+1,j} - 2T^{n}_{i,j} + T^{n}_{i-1,j}}{\Delta x^2}  + \frac{T^{n}_{i,j+1} - 2T^{n}_{i,j} + T^{n}_{i,j-1}}{\Delta y^2}\right]
$$

This will be the equation used to measure the temperature change in each cell of the matrix.

It is necessary to establish the behavior of the isolated edges. Ghost cells will be used represented as:

$$
T_{-1} = T_{0}
$$

In other words, the temperature of the preceding cell and that of the edge are equal. This leads to the following in the heat equation. Originally with $T_{-1}$ and $T_{0}$, it is:

$$
\left[\frac{T_{1,j} - 2T_{0,j} + T_{-1,j}}{\Delta x^2}  + \frac{T_{i,1} - 2T_{i,0} + T_{i,-1}}{\Delta y^2}\right]
$$

But because we have $T_{-1} = T_{0}$ it turns into:

$$
\left[\frac{T_{1,j} - T_{0,j}}{\Delta x^2}  + \frac{T_{i,1} - T_{i,0}}{\Delta y^2}\right]
$$

About the permanent heat source, it will be defined as:

Given a cell $(x_h, y_h)$

$$
T_{i,j} = T_h
$$

If $T_h = 100$ C°, that value will be permanent.