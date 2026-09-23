# Lucia
## Mycelium Propagation Simulation

### Objective
The objective of this project is to model and simulate the propagation of fungal mycelium under different environmental conditions.

The model will represent the ground as an environment and simulate how mycelium propagates over time based on factors such as:

- Soil humidity
- Temperature
- Nutrients available
- Spread probability
- And others (still thinking)

### Model
The soil will be represented using a cellular automaton, where each cell represents a portion of the soil. Each cell has a state that can change over time according to a set of rules based on its current state and the state of its neighbors.

Each cell can have different properties:
- Mycelium: Mycelium exists or not
- Nutrients: The amount of nutrients available in the cell
- Humidity: The amount of water available in the cell
- Temperature: The temperatre of the cell.

A cell can have more than one propierties

### Observations
Article: Mycelial response to spatiotemporal nutrien heterogeneity: A volocity-jump mathematical model
![Myceliyum](https://ars.els-cdn.com/content/image/1-s2.0-S1754504811000870-gr2.jpg)


### Parallelization
An idea is to explor the use of parallel programming to simulate the propagation of individual hypha simultaneously.

Each hypha will be treated as an independent task. The number of concurrent hypha will be limited acording to the number of available CPU cores.
