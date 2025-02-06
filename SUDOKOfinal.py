import random
import tkinter as tk
from copy import deepcopy

# Function to generate a solved Sudoku grid
def generate_sudoku():
    base = 3
    side = base * base

    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    def shuffle(s):
        return random.sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, side + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    return board

# Function to remove numbers to create a puzzle
def make_puzzle(board, difficulty=40):
    puzzle = deepcopy(board)
    removed = set()
    while len(removed) < difficulty:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if (row, col) not in removed:
            puzzle[row][col] = 0
            removed.add((row, col))
    return puzzle

# Faster Evolutionary Algorithm for solving Sudoku
def evolutionary_solver(puzzle):
    population_size = 100
    mutation_rate = 0.15
    max_generations = 1000

    def fitness(board):
        row_score = sum(len(set(row)) for row in board)
        col_score = sum(len(set(board[i][j] for i in range(9))) for j in range(9))
        block_score = sum(len(set(board[r+i][c+j] for i in range(3) for j in range(3))) for r in range(0, 9, 3) for c in range(0, 9, 3))
        return row_score + col_score + block_score

    def mutate(board):
        new_board = deepcopy(board)
        for i in range(9):
            empty_positions = [j for j in range(9) if puzzle[i][j] == 0]
            if len(empty_positions) >= 2 and random.random() < mutation_rate:
                a, b = random.sample(empty_positions, 2)
                new_board[i][a], new_board[i][b] = new_board[i][b], new_board[i][a]
        return new_board

    def create_individual():
        individual = deepcopy(puzzle)
        for i in range(9):
            missing = [n for n in range(1, 10) if n not in individual[i]]
            random.shuffle(missing)
            for j in range(9):
                if individual[i][j] == 0:
                    individual[i][j] = missing.pop()
        return individual

    population = [create_individual() for _ in range(population_size)]

    for generation in range(max_generations):
        population.sort(key=fitness, reverse=True)
        if fitness(population[0]) == 243:
            return population[0]

        next_generation = population[:20]  # Elitism
        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(population[:50], 2)
            child = mutate(deepcopy(parent1))
            next_generation.append(child)

        population = next_generation

    return population[0]

# GUI Implementation
class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.entries = []
        self.puzzle = None  # Initially set puzzle to None
        self.current_puzzle_type = None  # Tracks puzzle type (random or custom)
        self.generate_new_puzzle()
        self.build_grid()
        self.add_buttons()

    def generate_new_puzzle(self):
        self.solution = generate_sudoku()
        self.puzzle = make_puzzle(self.solution)
        self.current_puzzle_type = "random"  # Track that it's a random puzzle

    def build_grid(self):
        colors = ["#b3e5fc", "#c8e6c9", "#e1bee7"]  # Blue, Green, Purple
        self.entries.clear()  # Clear previous entries to build new grid
        for i in range(9):
            row_entries = []
            for j in range(9):
                color = colors[(i // 3 + j // 3) % len(colors)]
                entry = tk.Entry(self.root, width=5, font=('Arial', 20), justify='center', borderwidth=2, relief="ridge")
                entry.grid(row=i, column=j, padx=5, pady=5, ipadx=10, ipady=10)
                entry.config(bg=color)

                # Disable the input for pre-filled numbers in random puzzle
                if self.puzzle[i][j] != 0:
                    entry.insert(0, str(self.puzzle[i][j]))
                    entry.config(state='disabled', disabledforeground='black')
                else:
                    entry.config(state='normal')
                row_entries.append(entry)
            self.entries.append(row_entries)

    def add_buttons(self):
        random_button = tk.Button(self.root, text="Random Sudoku", command=self.random_sudoku)
        random_button.grid(row=9, column=0, columnspan=3, pady=10)

        custom_button = tk.Button(self.root, text="Custom Sudoku", command=self.create_custom_grid)
        custom_button.grid(row=9, column=3, columnspan=3, pady=10)

        solve_button = tk.Button(self.root, text="Solve", command=self.solve_puzzle)
        solve_button.grid(row=9, column=6, columnspan=3, pady=10)

    def solve_puzzle(self):
        # Collect puzzle from grid (user's input or random)
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                self.puzzle[i][j] = int(value) if value.isdigit() else 0

        solution = evolutionary_solver(self.puzzle)
        # Update grid with the solution
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(solution[i][j]))
                self.entries[i][j].config(fg='black')

    def random_sudoku(self):
        self.generate_new_puzzle()
        self.clear_grid()
        self.build_grid()

    def create_custom_grid(self):
        # Clear any existing grid
        self.clear_grid()
        # Set puzzle to empty (user will fill in)
        self.puzzle = [[0]*9 for _ in range(9)]
        self.current_puzzle_type = "custom"  # Track that it's a custom puzzle
        for i in range(9):
            for j in range(9):
                self.entries[i][j].config(state='normal')  # Enable all cells for user input

    def clear_grid(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].config(state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
