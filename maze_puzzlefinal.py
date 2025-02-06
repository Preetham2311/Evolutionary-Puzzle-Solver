import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
from PIL import Image, ImageTk

# Function to generate a random maze
def generate_maze(size=20):
    maze = np.ones((size, size), dtype=int)

    def carve_passages(cx, cy):
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 1 <= nx < size-1 and 1 <= ny < size-1 and maze[nx, ny] == 1:
                maze[cx+dx//2, cy+dy//2] = 0
                maze[nx, ny] = 0
                carve_passages(nx, ny)

    maze[1, 1] = 0
    carve_passages(1, 1)
    maze[size-2, size-2] = 0
    return maze

# Evolutionary algorithm to solve the maze
class EvolutionarySolver:
    def __init__(self, maze, start, end, population_size=50, generations=100, mutation_rate=0.1):
        self.maze = maze
        self.start = start
        self.end = end
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = self.create_population()

    def create_population(self):
        population = []
        for _ in range(self.population_size):
            path = self.generate_random_path()
            population.append(path)
        return population

    def generate_random_path(self):
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        path = []
        for _ in range(random.randint(10, 100)):
            path.append(random.choice(moves))
        return path

    def fitness(self, path):
        x, y = self.start
        for move in path:
            x += move[0]
            y += move[1]
            if x < 0 or x >= len(self.maze) or y < 0 or y >= len(self.maze[0]) or self.maze[x, y] == 1:
                return float('inf')
        return abs(x - self.end[0]) + abs(y - self.end[1])

    def select_parents(self):
        tournament_size = 5
        tournament = random.sample(self.population, tournament_size)
        tournament.sort(key=self.fitness)
        return tournament[0], tournament[1]

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(0, min(len(parent1), len(parent2)))
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child

    def mutate(self, path):
        if random.random() < self.mutation_rate:
            index = random.randint(0, len(path) - 1)
            path[index] = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        return path

    def evolve(self):
        for _ in range(self.generations):
            new_population = []
            for _ in range(self.population_size // 2):
                parent1, parent2 = self.select_parents()
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)
                new_population.append(self.mutate(child1))
                new_population.append(self.mutate(child2))
            self.population = new_population
            best_path = min(self.population, key=self.fitness)
            if self.fitness(best_path) == 0:
                return best_path
        return min(self.population, key=self.fitness)

# Main GUI Class
class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Puzzle Solver")
        self.size = 21  # Must be an odd number
        self.maze = generate_maze(self.size)
        self.start = (1, 1)
        self.end = (self.size-2, self.size-2)
        self.user_path = []
        self.current_position = self.start

        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()

        self.mouse_icon = "🐀"  # Mouse emoji
        self.cheese_icon = "🧀"  # Cheese emoji

        self.draw_maze()
        self.bind_keys()
        self.add_buttons()

        self.evolutionary_solver = EvolutionarySolver(self.maze, self.start, self.end)

        self.algorithm_solution = None  # Store the algorithm's solution

    def draw_maze(self):
        cell_size = 500 // self.size
        self.canvas.delete("all")
        for i in range(self.size):
            for j in range(self.size):
                color = "white" if self.maze[i][j] == 0 else "black"
                self.canvas.create_rectangle(j*cell_size, i*cell_size, (j+1)*cell_size, (i+1)*cell_size, fill=color)

        self.player = self.canvas.create_text(self.start[1]*cell_size + cell_size//2, self.start[0]*cell_size + cell_size//2, text=self.mouse_icon, font=("Arial", 20))
        self.canvas.create_text(self.end[1]*cell_size + cell_size//2, self.end[0]*cell_size + cell_size//2, text=self.cheese_icon, font=("Arial", 20))

    def bind_keys(self):
        self.root.bind("<Up>", lambda e: self.move(-1, 0))
        self.root.bind("<Down>", lambda e: self.move(1, 0))
        self.root.bind("<Left>", lambda e: self.move(0, -1))
        self.root.bind("<Right>", lambda e: self.move(0, 1))

    def move(self, dx, dy):
        new_pos = (self.current_position[0] + dx, self.current_position[1] + dy)
        if 0 <= new_pos[0] < self.size and 0 <= new_pos[1] < self.size and self.maze[new_pos] == 0:
            self.current_position = new_pos
            cell_size = 500 // self.size
            self.canvas.coords(self.player, new_pos[1]*cell_size + cell_size//2, new_pos[0]*cell_size + cell_size//2)
            self.user_path.append(new_pos)
            if new_pos == self.end:
                self.give_feedback()

    def add_buttons(self):
        solve_button = tk.Button(self.root, text="Solve", command=self.solve_maze)
        solve_button.pack()
        new_maze_button = tk.Button(self.root, text="New Maze", command=self.reset_maze)
        new_maze_button.pack()
        undo_button = tk.Button(self.root, text="Undo", command=self.undo_move)  # Undo button
        undo_button.pack()

    def solve_maze(self):
        self.algorithm_solution = self.evolutionary_solver.evolve()  # Store the solution
        self.compare_paths()

    def compare_paths(self):
        user_length = len(self.user_path)
        algorithm_length = len(self.algorithm_solution)
        messagebox.showinfo("Comparison", f"Your path length: {user_length}\nAlgorithm's path length: {algorithm_length}")

    def reset_maze(self):
        self.maze = generate_maze(self.size)
        self.start = (1, 1)
        self.end = (self.size-2, self.size-2)
        self.user_path = []
        self.current_position = self.start
        self.algorithm_solution = None  # Reset the solution when a new maze is generated
        self.draw_maze()

    def give_feedback(self):
        messagebox.showinfo("Success", "You have completed the maze!")

    def undo_move(self):
        """Undo the last move by resetting the position to the start."""
        self.current_position = self.start
        self.user_path = []  # Clear the user's path
        self.draw_maze()  # Redraw the maze with the mouse at the start position
        self.canvas.coords(self.player, self.start[1]*500//self.size + 500//self.size//2, self.start[0]*500//self.size + 500//self.size//2)

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
