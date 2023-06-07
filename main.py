# Course:               CS7375-W02 Artificial Intelligence
# Student name:         Adam Kangiser
# Student ID:           000681701
# Assignment number:    1
# Due Date:             June 16, 2023
# Signature:            Adam Kangiser
# Score:


import tkinter as tk  # For creating the GUI
import heapq  # For priority queue implementation
import random  # For generating random elements

# Define the Node class
class Node:
    def __init__(self, x, y, obstacle):
        self.x = x  # x-coordinate of the node
        self.y = y  # y-coordinate of the node
        self.obstacle = obstacle  # Indicates if the node is an obstacle
        self.g = float('inf')  # Cost from the start node to this node (initially infinite)
        self.h = float('inf')  # Heuristic cost from this node to the target node (initially infinite)
        self.f = float('inf')  # Total cost (g + h) of reaching the target node through this node (initially infinite)
        self.parent = None  # Parent node in the path

    def __lt__(self, other):
        return self.f < other.f
    # Enable comparison between Node objects based on their f values

# Define the ModelBasedAgent class
class ModelBasedAgent:
    def __init__(self, grid):
        self.grid = grid  # The grid containing nodes
        self.rows = len(grid)  # Number of rows in the grid
        self.cols = len(grid[0])  # Number of columns in the grid
        self.open_list = []  # List of nodes to be explored
        self.closed_list = []  # List of nodes already explored
        self.start_node = None  # Start node of the path
        self.target_node = None  # Target node of the path

    def heuristic(self, node):
        return abs(node.x - self.target_node.x) + abs(node.y - self.target_node.y)
        # Manhattan distance heuristic: the sum of the absolute differences in x and y coordinates

    def get_neighbors(self, node):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dx, dy in directions:
            new_x = node.x + dx
            new_y = node.y + dy

            if 0 <= new_x < self.rows and 0 <= new_y < self.cols:
                neighbor = self.grid[new_x][new_y]
                if not neighbor.obstacle:
                    neighbors.append(neighbor)
        # Check the neighboring nodes and add them to the list if they are valid and not obstacles

        return neighbors

    def reconstruct_path(self, node):
        path = []
        while node.parent:
            path.append((node.x, node.y))
            node = node.parent
        path.append((node.x, node.y))
        return path[::-1]
        # Reconstruct the path from the target node to the start node by following the parent pointers

    def a_star(self):
        heapq.heapify(self.open_list)  # Convert the open list to a priority queue
        heapq.heappush(self.open_list, self.start_node)  # Add the start node to the open list
        self.start_node.g = 0  # Set the cost from the start node to itself as 0
        self.start_node.h = self.heuristic(self.start_node)  # Calculate the heuristic cost for the start node
        self.start_node.f = self.start_node.g + self.start_node.h  # Calculate the total cost for the start node

        while self.open_list:
            current_node = heapq.heappop(self.open_list)  # Select the node with the lowest total cost from the open
            # list
            if current_node == self.target_node:  # If the target node is reached, return the path
                return self.reconstruct_path(current_node)

            self.closed_list.append(current_node)  # Add the current node to the closed list
            neighbors = self.get_neighbors(current_node)  # Get the neighboring nodes

            for neighbor in neighbors:
                if neighbor in self.closed_list:  # Skip the neighbor if it is already in the closed list
                    continue

                tentative_g = current_node.g + 1  # Calculate the tentative cost from the start node to the neighbor

                if tentative_g < neighbor.g:  # If the tentative cost is lower than the current cost to the neighbor
                    neighbor.parent = current_node  # Update the parent of the neighbor
                    neighbor.g = tentative_g  # Update the cost from the start node to the neighbor
                    neighbor.h = self.heuristic(neighbor)  # Calculate the heuristic cost for the neighbor
                    neighbor.f = neighbor.g + neighbor.h  # Calculate the total cost for the neighbor

                    if neighbor not in self.open_list:  # If the neighbor is not in the open list, add it
                        heapq.heappush(self.open_list, neighbor)

        return None  # If no path is found, return None

# Define the GridGUI class
class GridGUI:
    def __init__(self, grid):
        self.grid = grid  # The grid containing nodes
        self.rows = len(grid)  # Number of rows in the grid
        self.cols = len(grid[0])  # Number of columns in the grid
        self.agent = ModelBasedAgent(grid)  # Create an instance of the ModelBasedAgent

        self.agent.start_node = grid[0][0]  # Set the start node to the top-left corner of the grid
        self.agent.target_node = self.generate_random_target()  # Generate a random target node
        self.generate_random_obstacles()  # Generate random obstacles in the grid

        self.root = tk.Tk()  # Create the main window
        self.canvas = tk.Canvas(self.root, width=self.cols * 50, height=self.rows * 50)  # Create a canvas for drawing
        self.canvas.pack()

        self.draw_grid()  # Draw the grid on the canvas
        self.draw_obstacles()  # Draw the obstacles on the canvas
        self.draw_start_target()  # Draw the start and target nodes on the canvas
        self.draw_path()  # Draw the path from the start to the target node on the canvas

        self.root.mainloop()  # Start the main event loop of the GUI

    def generate_random_target(self):
        target_x = random.randint(0, self.rows - 1)  # Generate a random x-coordinate for the target node
        target_y = random.randint(0, self.cols - 1)  # Generate a random y-coordinate for the target node
        return self.grid[target_x][target_y]  # Return the target node from the grid

    def generate_random_obstacles(self):
        num_obstacles = random.randint(2, 3)  # Generate a random number of obstacles (2 to 3)

        for _ in range(num_obstacles):
            obstacle_x = random.randint(0, self.rows - 1)  # Generate a random x-coordinate for an obstacle
            obstacle_y = random.randint(0, self.cols - 1)  # Generate a random y-coordinate for an obstacle
            self.grid[obstacle_x][obstacle_y].obstacle = True  # Set the obstacle flag for the corresponding node in the grid
        # Generate random obstacles in the grid by setting the obstacle flag for random nodes

    def draw_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * 50  # Calculate the x-coordinate of the top-left corner of the rectangle
                y1 = i * 50  # Calculate the y-coordinate of the top-left corner of the rectangle
                x2 = x1 + 50  # Calculate the x-coordinate of the bottom-right corner of the rectangle
                y2 = y1 + 50  # Calculate the y-coordinate of the bottom-right corner of the rectangle

                if self.grid[i][j].obstacle:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='black')  # Draw a black rectangle for an obstacle
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='white')  # Draw a white rectangle for an empty node
        # Draw rectangles on the canvas to represent the nodes in the grid

    def draw_obstacles(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j].obstacle:
                    x = j * 50 + 25  # Calculate the x-coordinate of the center of the obstacle
                    y = i * 50 + 25  # Calculate the y-coordinate of the center of the obstacle
                    self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill='black')
                    # Draw a black oval for an obstacle
        # Draw ovals on the canvas to represent the obstacles in the grid

    def draw_start_target(self):
        start_x = self.agent.start_node.y * 50 + 25  # Calculate the x-coordinate of the center of the start node
        start_y = self.agent.start_node.x * 50 + 25  # Calculate the y-coordinate of the center of the start node
        self.canvas.create_oval(start_x - 12, start_y - 12, start_x + 12, start_y + 12, fill='green')
        # Draw a green oval for the start node

        target_x = self.agent.target_node.y * 50 + 25  # Calculate the x-coordinate of the center of the target node
        target_y = self.agent.target_node.x * 50 + 25  # Calculate the y-coordinate of the center of the target node
        self.canvas.create_oval(target_x - 12, target_y - 12, target_x + 12, target_y + 12, fill='red')
        # Draw a red oval for the target node
        # Draw ovals on the canvas to represent the start and target nodes

    def draw_path(self):
        path = self.agent.a_star()  # Find the path from the start to the target node using A* algorithm
        if path:
            for i in range(len(path) - 1):
                x1 = path[i][1] * 50 + 25  # Calculate the x-coordinate of the center of the current node in the path
                y1 = path[i][0] * 50 + 25  # Calculate the y-coordinate of the center of the current node in the path
                x2 = path[i + 1][1] * 50 + 25  # Calculate the x-coordinate of the center of the next node in the path
                y2 = path[i + 1][0] * 50 + 25  # Calculate the y-coordinate of the center of the next node in the path
                self.canvas.create_line(x1, y1, x2, y2, width=3, fill='blue')
                # Draw a blue line connecting the centers of adjacent nodes in the path
        # Draw lines on the canvas to represent the path from the start to the target node

# Example usage
grid = [[Node(i, j, False) for j in range(5)] for i in range(5)]  # Create a 5x5 grid of nodes

gui = GridGUI(grid)  # Create an instance of the GridGUI class with the grid
