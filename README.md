# Lucia
## Forest Fire Spread Simulation

## Objective
The objective of this project is to model the spread of a forest fire and simulate how it propagates under different enviromental conditions.

The model will represent the forest as a environment and simulate how fire propagates over time based on factors such as:

- Wind speed and direction
- Terrain slope
- Fire propagation probability
- Vegetation
- Humidity

## Model
The forest will be represented using a cellular automaton, where each cell represents a portion of terrain, this model represents a system as a grid of individual cells. Each cell has a state that can change over time acording to a set of rules based on its current state and the states of its neighbors.

Each cell can have different states:
- Empty: No vegetation
- Unburned: Not in fire with vegetation
- Burning: Currently burning
- Burned: Previously burned

## Observations
There is a algorithm published in 1972 named "Rothermel Surface Fire Spread Model", that can predict the velocity of propagation and the intensity of a fire.
