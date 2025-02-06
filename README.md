# Evolutionary Puzzle Solver

A comprehensive puzzle-solving application that uses evolutionary algorithms to solve various classic puzzles. The application features an interactive GUI launcher, multiple puzzle types, and an integrated chatbot for user assistance.

## Features

### 1. Multiple Puzzle Types
- **Rubik's Cube**
  - 3D visualization using VPython
  - Interactive controls for cube manipulation
  - Automatic solving using evolutionary algorithms
  - Real-time solution visualization

- **Sudoku**
  - Play mode for manual solving
  - Automatic solver for custom puzzles
  - Interactive grid interface

- **Maze**
  - Procedurally generated mazes
  - Play mode for manual solving
  - Automatic pathfinding using genetic algorithms
  - Visual representation of solution path

- **N-Queens**
  - Population-based evolutionary solver
  - Real-time visualization of solution progress
  - Customizable solver parameters

- **Tic-Tac-Toe**
  - Classic gameplay implementation
  - Play against AI/Human opponent

### 2. Integrated Chatbot
- Real-time assistance for users
- Answers queries about puzzle mechanics
- Provides hints and strategies
- Helps troubleshoot issues

### 3. User Interface
- Modern, intuitive GUI design
- Elegant color scheme with Coral Grey theme
- Smooth animations and transitions
- Responsive button controls
- Consistent layout across all puzzles

## Requirements

- Python 3.x
- Required packages:
  - pygame
  - numpy
  - tkinter
  - vpython
  - kociemba (for Rubik's Cube solving)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/evolutionary-puzzle-solver.git
cd evolutionary-puzzle-solver
```

2. Install required packages:
```bash
pip install pygame numpy vpython kociemba
```

## Usage

1. Launch the main application:
```bash
python main_launcher.py
```

2. Select a puzzle from the main menu:
   - Click on the respective puzzle card
   - Choose between "Play" or "Solve" modes where available

3. For solving custom puzzles:
   - Select the puzzle type
   - Input your puzzle configuration
   - Click "Solve" to see the solution

4. Access the chatbot:
   - Click the "Chatbot" button at the bottom of the launcher
   - Type your question or query
   - Receive instant assistance

## Puzzle-Specific Features

### Rubik's Cube
- Interactive 3D visualization
- Support for standard cube notation (F, R, B, L, U, D)
- One-click scramble function
- Step-by-step solution display

### Maze
- Random maze generation
- Evolutionary pathfinding algorithm
- Visual solution path

### N-Queens
- Customizable evolutionary parameters:
  - Population size
  - Mutation rate
- Real-time solution visualization

### Sudoku
- Standard 9x9 grid
- Input validation
- Solution checking

## Technical Details

### Evolutionary Algorithms
The project implements various evolutionary and genetic algorithms:
- Population-based optimization
- Fitness function evaluation
- Mutation and crossover operations
- Selection mechanisms

### Visualization
- Real-time solution visualization
- Interactive controls
- Dynamic updates

## License

This project is licensed under the MIT License - see the LICENSE file for details.


