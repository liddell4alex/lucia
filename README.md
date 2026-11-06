# Lucia
## Modeling heat transfer in a metal plate

### Author
**Name:** Alejandro Cons Andable <br>
**Affiliation:** Universidad Nacional Autónoma de México (UNAM) <br>
**Contact:** alexmixsep@gmail.com <br>

### Objective
The objective of this project is to model and simulate the propagation of heat in a metal plate over time.

The metal plate will have an initial temperature. An initial point of heat source will begin to warm the plate, and we will observe how the heat is distribuited throughout the plate.

I will use the physical phenomenon known as thermal conduction.

### Model
**Static conditions:**
- Rectangular plate of variable dimensions.
- Plate made of aluminum.
- Specific heat capacity.
- Using thermal conduction.
- Represented on a 2D grid.
- Insulated edges— meaning heat cannot escape.

**Initial conditions:**
- Plate dimensions $$Dims = (L_x, L_y)$$
- Initial plate temperature $$T_0$$
- Heat source temperature $$T_h$$
- Heat source starting point $$P = (x_h, y_h)$$

### Matematical issues
I will use the two-dimensional heat equation:

$$
\frac{\partial T}{\partial t} = \alpha\left(\frac{\partial^2T}{\partial x^2} + \frac{\partial^2T}{\partial y^2}\right)
$$

Where:
- $\frac{\partial T}{\partial t}$: Change in temperature over time.

- $\frac{\partial^2T}{\partial x^2}$: Spatial variation of temperature in x.


Understanding **thermal diffusivity**.
$$
\alpha = \frac{k}{\rho\,c_p}
$$
It indicates how quickly a temperature variation spreads through a material.
- $k$: Thermal conductivity.
- $\rho$: Material density.
- $c_p$: Specific heat capacity (Of the aluminum in this case).





### Parallelization
