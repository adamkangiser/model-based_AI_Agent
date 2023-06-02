import tkinter as tk
import heapq
import random


class Node:
    def __init__(self, x, y, obstacle):
        self.x = x
        self.y = y
        self.obstacle = obstacle
        self.g = float('inf')
        self.h = float('inf')
        self.f = float('inf')
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f


class ModelBasedAgent:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.open_list = []
        self.closed_list = []
        self.start_node = None
        self.target_node = None

    def heuristic(self, node):
        return abs(node.x - self.target_node.x) + abs(node.y - self.target_node.y)

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

        return neighbors

    def reconstruct_path(self, node):
        path = []
        while node.parent:
            path.append((node.x, node.y))
            node = node.parent
        path.append((node.x, node.y))
        return path[::-1]

    def a_star(self):
        heapq.heapify(self.open_list)
        heapq.heappush(self.open_list, self.start_node)
        self.start_node.g = 0
        self.start_node.h = self.heuristic(self.start_node)
        self.start_node.f = self.start_node.g + self.start_node.h

        while self.open_list:
            current_node = heapq.heappop(self.open_list)
            if current_node == self.target_node:
                return self.reconstruct_path(current_node)

            self.closed_list.append(current_node)
            neighbors = self.get_neighbors(current_node)

            for neighbor in neighbors:
                if neighbor in self.closed_list:
                    continue

                tentative_g = current_node.g + 1

                if tentative_g < neighbor.g:
                    neighbor.parent = current_node
                    neighbor.g = tentative_g
                    neighbor.h = self.heuristic(neighbor)
                    neighbor.f = neighbor.g + neighbor.h

                    if neighbor not in self.open_list:
                        heapq.heappush(self.open_list, neighbor)

        return None


class GridGUI:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.agent = ModelBasedAgent(grid)

        self.agent.start_node = grid[0][0]
        self.agent.target_node = self.generate_random_target()
        self.generate_random_obstacles()

        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.cols * 50, height=self.rows * 50)
        self.canvas.pack()

        self.draw_grid()
        self.draw_obstacles()
        self.draw_start_target()
        self.draw_path()

        self.root.mainloop()

    def generate_random_target(self):
        target_x = random.randint(0, self.rows - 1)
        target_y = random.randint(0, self.cols - 1)
        return self.grid[target_x][target_y]

    def generate_random_obstacles(self):
        num_obstacles = random.randint(2, 3)  # Adjust the number of obstacles as desired

        for _ in range(num_obstacles):
            obstacle_x = random.randint(0, self.rows - 1)
            obstacle_y = random.randint(0, self.cols - 1)
            self.grid[obstacle_x][obstacle_y].obstacle = True

    def draw_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * 50
                y1 = i * 50
                x2 = x1 + 50
                y2 = y1 + 50

                if self.grid[i][j].obstacle:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='black')
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='white')

    def draw_obstacles(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j].obstacle:
                    x = j * 50 + 25
                    y = i * 50 + 25
                    self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill='black')

    def draw_start_target(self):
        start_x = self.agent.start_node.y * 50 + 25
        start_y = self.agent.start_node.x * 50 + 25
        self.canvas.create_oval(start_x - 12, start_y - 12, start_x + 12, start_y + 12, fill='green')

        target_x = self.agent.target_node.y * 50 + 25
        target_y = self.agent.target_node.x * 50 + 25
        self.canvas.create_oval(target_x - 12, target_y - 12, target_x + 12, target_y + 12, fill='red')

    def draw_path(self):
        path = self.agent.a_star()
        if path:
            for i in range(len(path) - 1):
                x1 = path[i][1] * 50 + 25
                y1 = path[i][0] * 50 + 25
                x2 = path[i + 1][1] * 50 + 25
                y2 = path[i + 1][0] * 50 + 25
                self.canvas.create_line(x1, y1, x2, y2, width=3, fill='blue')


# Example usage
grid = [[Node(i, j, False) for j in range(4)] for i in range(4)]  # Create a 4x4 grid of nodes

gui = GridGUI(grid)
