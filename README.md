# A* Pathfinding Algorithm with GUI

This Python code demonstrates the A* pathfinding algorithm using a graphical user interface (GUI) built with the tkinter library. The algorithm finds the shortest path from a start node to a target node on a grid, considering obstacles.

## Code Components

- `Node` class: Represents a node on the grid with coordinates, obstacle flag, cost, and parent information.
- `ModelBasedAgent` class: Implements the A* algorithm to find the shortest path from the start node to the target node.
- `GridGUI` class: Creates a GUI window and handles the visualization of the grid, obstacles, start/target nodes, and the path.

## Usage

1. Run the code.
2. The grid GUI window will appear, displaying a grid with obstacles, start and target nodes.
3. The A* algorithm will find the shortest path from the start to the target node.
4. The shortest path will be displayed as a blue line connecting the centers of adjacent nodes.
5. Close the GUI window to exit the program.

## Example

```python
grid = [[Node(i, j, False) for j in range(5)] for i in range(5)]  # Create a 5x5 grid of nodes

gui = GridGUI(grid)  # Create an instance of the GridGUI class with the grid
```

This example creates a 5x5 grid of nodes and visualizes it using the GUI. You can customize the grid size and obstacle configuration to explore different scenarios.

## Note

The A* algorithm uses the Manhattan distance heuristic to estimate the cost from each node to the target node. It explores nodes with lower total costs (g + h) first, gradually expanding towards the target node. The algorithm guarantees the shortest path if it exists.

The GUI allows you to visualize the grid, obstacles, start and target nodes, and the shortest path. You can modify the code to create custom grids, change the number of obstacles, and further enhance the visualization.
