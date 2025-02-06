import random
import numpy as np
import tkinter as tk
from tkinter import messagebox, Frame
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
    for _ in range(difficulty):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while puzzle[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        puzzle[row][col] = 0
    return puzzle

# Solution Checking Function
def is_valid_solution(user_solution):
    for i in range(9):
        if len(set(user_solution[i])) < 9:
            return False, f"Error in row {i+1}"
        if len(set([user_solution[j][i] for j in range(9)])) < 9:
            return False, f"Error in column {i+1}"

    for r in range(0, 9, 3):
        for c in range(0, 9, 3):
            square = [user_solution[r+i][c+j] for i in range(3) for j in range(3)]
            if len(set(square)) < 9:
                return False, f"Error in 3x3 block at ({r+1}, {c+1})"
    return True, "Correct solution!"

# GUI Implementation
class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.root.configure(bg="#f4f4f4")

        self.solution = generate_sudoku()
        self.puzzle = make_puzzle(self.solution)
        self.entries = []

        self.create_title()
        self.build_grid()
        self.add_buttons()

    def create_title(self):
        title_label = tk.Label(self.root, text="Sudoku Puzzle", font=("Arial", 20, "bold"), bg="#f4f4f4", fg="#333")
        title_label.pack(pady=10)

    def build_grid(self):
        grid_frame = Frame(self.root, bg="#ffffff", bd=3, relief="solid")
        grid_frame.pack(pady=10)

        # Define pastel colors for each sub-grid
        sub_grid_colors = [
            ["#FFD1DC", "#E0BBE4", "#FFDFBA"], 
            ["#B5EAD7", "#C7CEEA", "#FFDAC1"], 
            ["#FFB7B2", "#FF9AA2", "#B5EAD7"]
        ]

        for i in range(9):
            row_entries = []
            for j in range(9):
                # Determine the background color based on 3x3 sub-grid
                bg_color = sub_grid_colors[i // 3][j // 3]

                entry = tk.Entry(grid_frame, width=4, font=("Arial", 16), justify='center', 
                                 relief="solid", bd=1, bg=bg_color)
                entry.grid(row=i, column=j, padx=2, pady=2)
                if self.puzzle[i][j] != 0:
                    entry.insert(0, str(self.puzzle[i][j]))
                    entry.config(state='disabled', disabledbackground=bg_color, disabledforeground="black")
                row_entries.append(entry)
            self.entries.append(row_entries)

    def add_buttons(self):
        button_frame = tk.Frame(self.root, bg="#f4f4f4")
        button_frame.pack(pady=10)

        submit_button = tk.Button(button_frame, text="Check Solution", command=self.check_solution,
                                  font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5)
        submit_button.grid(row=0, column=0, padx=10)

        reset_button = tk.Button(button_frame, text="Reset", command=self.reset_board,
                                 font=("Arial", 14, "bold"), bg="#f44336", fg="white", padx=10, pady=5)
        reset_button.grid(row=0, column=1, padx=10)

    def check_solution(self):
        user_solution = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.entries[i][j].get()
                row.append(int(value) if value.isdigit() else 0)
            user_solution.append(row)

        is_correct, feedback = is_valid_solution(user_solution)
        if is_correct:
            messagebox.showinfo("Success", feedback)
        else:
            messagebox.showerror("Error", feedback)

    def reset_board(self):
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    self.entries[i][j].delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
