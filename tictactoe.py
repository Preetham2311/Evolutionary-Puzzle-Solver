import tkinter as tk
import random
import copy

# Game settings
BOARD_SIZE = 3
EMPTY = ' '
X = 'X'
O = 'O'

# Evolutionary Algorithm settings
MUTATION_RATE = 0.2
POPULATION_SIZE = 100
GENERATIONS = 100
TOURNAMENT_SIZE = 10  # Number of AI strategies competing against each other in each round

# Tic-Tac-Toe class
class TicTacToe:
    def __init__(self):
        self.board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = X
        self.game_over = False
        self.winner = None
    
    def make_move(self, row, col):
        if self.board[row][col] == EMPTY and not self.game_over:
            self.board[row][col] = self.current_player
            if self.check_winner():
                self.game_over = True
            elif self.is_full():
                self.game_over = True  # It's a tie if the board is full and no winner
            self.current_player = O if self.current_player == X else X
    
    def check_winner(self):
        # Check rows, columns, and diagonals
        for i in range(BOARD_SIZE):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != EMPTY:
                self.winner = self.board[i][0]
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != EMPTY:
                self.winner = self.board[0][i]
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != EMPTY:
            self.winner = self.board[0][0]
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != EMPTY:
            self.winner = self.board[0][2]
            return True
        return False
    
    def reset(self):
        self.board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = X
        self.game_over = False
        self.winner = None
    
    def is_full(self):
        for row in self.board:
            if EMPTY in row:
                return False
        return True

class TicTacToeAI:
    def __init__(self):
        self.population = self.initialize_population()
    
    def initialize_population(self):
        # Randomly generate strategies
        return [self.random_strategy() for _ in range(POPULATION_SIZE)]
    
    def random_strategy(self):
        # Generate a strategy randomly for the AI (for simplicity, it's a random move strategy)
        return [[random.choice([EMPTY, X, O]) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    def mutate(self, strategy):
        # Apply mutations to the strategy
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if random.random() < MUTATION_RATE:
                    strategy[i][j] = random.choice([EMPTY, X, O])
        return strategy
    
    def select_best_strategy(self, fitness_scores):
        # Select strategies based on their fitness scores
        max_score = max(fitness_scores)
        best_strategies = [self.population[i] for i in range(POPULATION_SIZE) if fitness_scores[i] == max_score]
        return random.choice(best_strategies)
    
    def evolve(self, fitness_scores):
        # Create the next generation by selecting the best strategies and applying mutation
        new_population = []
        for _ in range(POPULATION_SIZE):
            parent = self.select_best_strategy(fitness_scores)
            child = self.mutate(copy.deepcopy(parent))  # Create a mutated copy of the strategy
            new_population.append(child)
        self.population = new_population
    
    def evaluate_fitness(self, strategy, board):
        # Fitness function: Evaluate how well a strategy performs
        score = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == EMPTY and strategy[i][j] == X:
                    score += 1  # Reward strategies that place X in empty spots
        return score
    
    def get_best_move(self, board):
        # Evaluate all strategies and return the best move
        fitness_scores = [self.evaluate_fitness(strategy, board) for strategy in self.population]
        best_strategy = self.select_best_strategy(fitness_scores)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if best_strategy[i][j] == X and board[i][j] == EMPTY:
                    return i, j
        return random.choice([(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == EMPTY])

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Evolution")
        self.root.configure(bg="#212121")  # Set dark background color
        
        # Initialize default mode to Human vs Human
        self.game_mode = "human_vs_human"
        self.game = TicTacToe()
        self.ai = None
        
        self.buttons = {}
        self.create_mode_buttons()
    
    def create_mode_buttons(self):
        # Mode buttons for Human vs Human and Human vs Computer
        self.human_vs_human_button = tk.Button(self.root, text="Human vs Human", width=20, height=2, font=('Helvetica', 14, 'bold'), bg="#D32F2F", fg="black", activebackground="#C62828", command=self.set_human_vs_human)
        self.human_vs_human_button.grid(row=0, column=0, pady=10)
        
        self.human_vs_computer_button = tk.Button(self.root, text="Human vs Computer", width=20, height=2, font=('Helvetica', 14, 'bold'), bg="#1976D2", fg="black", activebackground="#1565C0", command=self.set_human_vs_computer)
        self.human_vs_computer_button.grid(row=0, column=2, pady=10)
        
        self.reset_button = tk.Button(self.root, text="Restart", width=20, height=2, font=('Helvetica', 14, 'bold'), bg="#FF9800", fg="black", activebackground="#F57C00", command=self.restart_game)
        self.reset_button.grid(row=1, column=0, columnspan=4, pady=10)
    
    def set_human_vs_human(self):
        self.game_mode = "human_vs_human"
        self.game = TicTacToe()
        self.ai = None
        self.create_game_board()
    
    def set_human_vs_computer(self):
        self.game_mode = "human_vs_computer"
        self.game = TicTacToe()
        self.ai = TicTacToeAI()  # Initialize AI for Human vs Computer mode
        self.create_game_board()
    
    def create_game_board(self):
        for widget in self.root.winfo_children():
            widget.grid_forget()
        
        self.create_mode_buttons()  # Recreate mode buttons
        
        # Create game board buttons with color
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                btn = tk.Button(self.root, text=EMPTY, width=10, height=3, font=('Helvetica', 24, 'bold'),
                                bg="#263238", fg="black", activebackground="#37474F", bd=3,
                                command=lambda i=i, j=j: self.on_button_click(i, j))
                btn.grid(row=i + 2, column=j)
                self.buttons[(i, j)] = btn
    
    def update_button(self, row, col):
        self.buttons[(row, col)].config(text=self.game.board[row][col], fg="green" if self.game.board[row][col] == X else "blue")
    
    def on_button_click(self, row, col):
        if not self.game.game_over and self.game.board[row][col] == EMPTY:
            self.game.make_move(row, col)
            self.update_button(row, col)
            if self.game.game_over:
                self.show_winner()
            elif self.game.current_player == O and self.game_mode == "human_vs_computer":  # AI's turn
                self.ai_turn()
    
    def ai_turn(self):
        row, col = self.ai.get_best_move(self.game.board)
        self.game.make_move(row, col)
        self.update_button(row, col)
        if self.game.game_over:
            self.show_winner()
    
    def show_winner(self):
        if self.game.winner:
            result = f"{self.game.winner} wins!"
        else:
            result = "It's a draw!"
        
        result_label = tk.Label(self.root, text=result, font=('Helvetica', 16, 'bold'), bg="#212121", fg="lime" if self.game.winner == X else "cyan")
        result_label.grid(row=BOARD_SIZE + 2, column=0, columnspan=BOARD_SIZE, pady=10)

    def restart_game(self):
        self.game.reset()
        self.create_game_board()

# Main function to start the game
def main():
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
