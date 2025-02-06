import tkinter as tk
from tkinter import ttk
import random
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

class EvolutionaryNQueens:
    def __init__(self, N, population_size=100, mutation_rate=0.1):
        self.N = N
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.best_solution = None
        self.best_fitness = float('-inf')

    def create_individual(self):
        return random.sample(range(self.N), self.N)

    def initialize_population(self):
        return [self.create_individual() for _ in range(self.population_size)]

    def fitness(self, individual):
        conflicts = 0
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if abs(i - j) == abs(individual[i] - individual[j]):
                    conflicts += 1
        max_conflicts = (self.N * (self.N - 1)) // 2
        return max_conflicts - conflicts

    def select_parent(self, population, fitness_scores):
        tournament = random.sample(range(len(population)), 3)
        return max(tournament, key=lambda i: fitness_scores[i])

    def crossover(self, parent1, parent2):
        point1, point2 = sorted(random.sample(range(self.N), 2))
        child = [-1] * self.N
        child[point1:point2] = parent1[point1:point2]
        remaining = [x for x in parent2 if x not in child]
        child = [x if x != -1 else remaining.pop(0) for x in child]
        return child

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(self.N), 2)
            individual[i], individual[j] = individual[j], individual[i]
        return individual

    def solution_to_board(self, solution):
        return [[1 if solution[j] == i else 0 for j in range(self.N)] for i in range(self.N)]

    async def solve(self, max_generations=1000, update_callback=None):
        population = self.initialize_population()
        for generation in range(max_generations):
            fitness_scores = [self.fitness(ind) for ind in population]
            best_idx = max(range(len(fitness_scores)), key=lambda i: fitness_scores[i])
            
            if fitness_scores[best_idx] > self.best_fitness:
                self.best_fitness = fitness_scores[best_idx]
                self.best_solution = population[best_idx]
                if update_callback:
                    await update_callback(self.solution_to_board(self.best_solution))
            
            if self.best_fitness == (self.N * (self.N - 1)) // 2:
                return self.solution_to_board(self.best_solution)

            new_population = []
            for _ in range(self.population_size // 2):
                p1, p2 = self.select_parent(population, fitness_scores), self.select_parent(population, fitness_scores)
                c1, c2 = self.crossover(population[p1], population[p2]), self.crossover(population[p2], population[p1])
                new_population.extend([self.mutate(c1), self.mutate(c2)])
            
            population = new_population
        return self.solution_to_board(self.best_solution)

class NQueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Solver")
        self.root.geometry("600x700")
        
        self.n_var = tk.StringVar(value="8")
        self.pop_size_var = tk.StringVar(value="100")
        self.mutation_rate_var = tk.StringVar(value="0.1")
        
        frame = ttk.Frame(root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="N-Queens Solver", font=("Arial", 16, "bold")).pack(pady=10)
        
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(input_frame, text="Board Size (N):").grid(row=0, column=0, padx=5, pady=5)
        self.n_entry = ttk.Entry(input_frame, textvariable=self.n_var, width=5)
        self.n_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Population Size:").grid(row=1, column=0, padx=5, pady=5)
        self.pop_size_entry = ttk.Entry(input_frame, textvariable=self.pop_size_var, width=5)
        self.pop_size_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Mutation Rate:").grid(row=2, column=0, padx=5, pady=5)
        self.mutation_rate_entry = ttk.Entry(input_frame, textvariable=self.mutation_rate_var, width=5)
        self.mutation_rate_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.solve_button = ttk.Button(frame, text="Solve", command=self.solve)
        self.solve_button.pack(pady=10)
        
        self.canvas = tk.Canvas(frame, background="white", width=500, height=500)
        self.canvas.pack(pady=10)
        
        self.loop = asyncio.new_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=1)
        
    def draw_board(self, board):
        self.canvas.delete("all")
        size = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // len(board)
        for i in range(len(board)):
            for j in range(len(board)):
                x1, y1, x2, y2 = j * size, i * size, (j + 1) * size, (i + 1) * size
                color = "#f0f0f0" if (i + j) % 2 == 0 else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                if board[i][j]:
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="♕", font=("Arial", size // 2), fill="black")
    
    async def update_display(self, board):
        self.draw_board(board)
        self.root.update()
        await asyncio.sleep(0.1)
    
    def solve(self):
        N = int(self.n_var.get())
        population_size = int(self.pop_size_var.get())
        mutation_rate = float(self.mutation_rate_var.get())
        solver = EvolutionaryNQueens(N, population_size, mutation_rate)
        asyncio.run_coroutine_threadsafe(solver.solve(update_callback=self.update_display), self.loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensGUI(root)
    thread = threading.Thread(target=app.loop.run_forever, daemon=True)
    thread.start()
    root.mainloop()
    app.loop.stop()
