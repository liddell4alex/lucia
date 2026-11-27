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

First 