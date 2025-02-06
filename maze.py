import numpy as np
import random
import pygame
from pygame.locals import *
import time

###### Parameters
#### Graphism
window_length = 640
window_width = 480
maze_color = (255, 0, 0)
background_color = (255, 255, 255)
entrance_color = (0, 255, 0)
exit_color = (0, 0, 255)
button_color = (100, 100, 100)
button_hover_color = (150, 150, 150)
show_path_color = (0, 0, 0)  # Black path

#### Back
shape = (10, 10)
holes = 5
number_of_generations = 1000
pop_card = 3000
elite = 0.01
mortality = 0.4
mutation_rate = 0.4
max_moves = 100

def manh_dist(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class Game:
    def __init__(self, shape=(3, 7), holes=0):
        self.dist_factor = 5
        self.exploration_factor = 6
        self.wall_penality = 2
        self.entrance_penality = 50
        self.exit_reward = 100
        
        self.entrance = (1 + 2 * random.randint(0, shape[0] - 1), 0)
        self.exit = (1 + 2 * random.randint(0, shape[0] - 1), shape[1] * 2)
        
        self.maze = np.zeros((shape[0] * 2 + 1, shape[1] * 2 + 1))
        
        # delimitations
        self.maze[0] = 1
        self.maze[-1] = 1
        self.maze[:, 0] = 1
        self.maze[:, -1] = 1
        
        def recursive_maze(maze):
            if maze.shape[0] <= 1 and maze.shape[1] <= 1:
                return []
                
            if maze.shape[0] < maze.shape[1]:
                verti = 2 * random.randint(0, maze.shape[1] // 2 - 1) + 1
                hori = 2 * random.randint(0, maze.shape[0] // 2)
                maze[:, verti] = 1
                maze[hori, verti] = 0
                return [maze[:, :verti], maze[:, verti + 1:]]
            else:
                hori = 2 * random.randint(0, maze.shape[0] // 2 - 1) + 1
                verti = 2 * random.randint(0, maze.shape[1] // 2)
                maze[hori] = 1
                maze[hori, verti] = 0
                return [maze[:hori, :], maze[hori + 1:, :]]
        
        queue = [self.maze[1:-1, 1:-1]]
        while queue:
            sub = queue.pop(0)
            temp = recursive_maze(sub)
            queue.extend(temp)
            
        for _ in range(holes):
            if random.random() < 0.5:
                verti = 2 * random.randint(1, self.maze.shape[1] // 2 - 1)
                hori = 2 * random.randint(0, self.maze.shape[0] // 2 - 1) + 1
            else:
                hori = 2 * random.randint(1, self.maze.shape[0] // 2 - 1)
                verti = 2 * random.randint(0, self.maze.shape[1] // 2 - 1) + 1
                
            if self.maze[hori, verti] == 1:
                self.maze[hori, verti] = 0
                
        self.maze[self.entrance] = 2
        self.maze[self.exit] = 3
        
    def play(self, player, record=False):
        position = self.entrance
        score = 0
        memo = [position]
        
        for i in player.genome:
            if i == 0:
                temp = (position[0], position[1] + 1)
            if i == 1:
                temp = (position[0] + 1, position[1])
            if i == 2:
                temp = (position[0], position[1] - 1)
            if i == 3:
                temp = (position[0] - 1, position[1])
            if i == 4:
                temp = position
                
            if temp[1] >= 0 and temp[1] < self.maze.shape[1]:
                if self.maze[temp] == 1:
                    score -= self.wall_penality
                if self.maze[temp] == 0:
                    position = temp
                if self.maze[temp] == 2:
                    position = temp
                    score -= self.entrance_penality
                if self.maze[temp] == 3:
                    score += self.exit_reward
                    position = temp
                    
                memo.append(position)
            else:
                score -= self.wall_penality
                
        score += self.exploration_factor * len(set(memo))
        score -= self.dist_factor * manh_dist(position, self.exit)
        
        if record:
            return score, position, memo
        return score, position
        
    def print_maze(self):
        print(self.maze)

class Sample:
    def __init__(self, creation="random", max_length=30, genome=[], parent1=None, parent2=None):
        self.score = None
        self.end_position = None
        
        if creation == "random":
            self.genome = [random.randint(0, 4) for _ in range(max_length)]
        elif creation == "genome":
            self.genome = genome
        elif creation == "cross over":
            if parent1 is None or parent2 is None:
                raise NameError("Parents are not defined")
            if parent1.score > parent2.score:
                begin = parent1
                end = parent2
            else:
                begin = parent2
                end = parent1
            cross_point = random.randint(0, len(parent1.genome))
            self.genome = begin.genome[:cross_point] + end.genome[cross_point:]
        else:
            raise NameError("Mode of creation not defined")
            
    def mutate(self):
        x1 = random.randint(0, len(self.genome))
        x2 = random.randint(0, (len(self.genome) - x1))
        
        for k in range(x1, x1 + x2):
            temp = random.randint(0, 6)
            if temp < 5:
                self.genome[k] = temp
            elif k > 0:
                self.genome[k] = self.genome[k - 1]

class GA:
    def __init__(self, game, genome_length=None, pop_card=5000, elite=0.01, mortality=0.4, mutation_rate=0.2):
        self.game = game
        self.mutation_rate = mutation_rate
        self.pop_card = pop_card
        self.elite_card = int(elite * pop_card)
        self.death_card = int(mortality * pop_card)
        self.pop = [Sample(creation="random", max_length=genome_length) for _ in range(pop_card)]
        
        for sample in self.pop:
            temp = game.play(sample)
            sample.score = temp[0]
            sample.end_position = temp[1]
            
        self.pop.sort(key=lambda sample: sample.score, reverse=True)
        
    def cross_over_step(self, number):
        parent1 = random.randint(0, self.pop_card - 1)
        parent2 = random.randint(0, self.pop_card - 1)
        self.pop[number] = Sample(creation="cross over", parent1=self.pop[parent1], parent2=self.pop[parent2])
        temp = self.game.play(self.pop[number])
        self.pop[number].score = temp[0]
        self.pop[number].end_position = temp[1]
        
    def mutation_step(self, number):
        if random.random() < self.mutation_rate:
            self.pop[number].mutate()
            temp = self.game.play(self.pop[number])
            self.pop[number].score = temp[0]
            self.pop[number].end_position = temp[1]
            
    def do_gen(self):
        for k in range(self.pop_card - self.death_card, self.pop_card):
            self.cross_over_step(k)
        for k in range(self.elite_card, self.pop_card):
            self.mutation_step(k)
        self.pop.sort(key=lambda sample: sample.score, reverse=True)

# Visualization functions
def draw_maze(window, maze, square_size, maze_color):
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == 1:
                pygame.draw.rect(window, maze_color, 
                               (j * square_size, i * square_size, square_size, square_size))
    pygame.display.update()

def clear_maze(window, maze, square_size, back_ground_color):
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] != 1:
                pygame.draw.rect(window, back_ground_color,
                               (j * square_size, i * square_size, square_size, square_size))
    pygame.display.update()

def show_path(window, game, sample, square_size, show_path_color):
    memo = game.play(sample, record=True)[2]
    for pos in memo:
        pygame.draw.rect(window, show_path_color,
                        (pos[1] * square_size, pos[0] * square_size, square_size, square_size))
    pygame.display.update()

def show_gen(gen, algo, game, time=None):
    print("--------------------------------------------")
    print("benchmark of generation", gen)
    if time is not None:
        print("time (s) :", time)
    print("best score :", algo.pop[0].score)
    print("Manhattan distance :", manh_dist(algo.pop[0].end_position, game.exit))
    print("--------------------------------------------")

def draw_button(window, text, position, size, color):
    pygame.draw.rect(window, color, (*position, *size))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(position[0] + size[0]/2, position[1] + size[1]/2))
    window.blit(text_surface, text_rect)
    pygame.display.update()

def is_point_inside_button(point, button_pos, button_size):
    return (button_pos[0] <= point[0] <= button_pos[0] + button_size[0] and
            button_pos[1] <= point[1] <= button_pos[1] + button_size[1])

def init_game():
    game = Game(shape=shape, holes=holes)
    algo = GA(game, genome_length=max_moves, pop_card=pop_card, elite=elite,
              mortality=mortality, mutation_rate=mutation_rate)
    return game, algo

def main():
    pygame.init()
    
    # Init game
    game, algo = init_game()
    square_size = min(window_length // game.maze.shape[1], window_width // game.maze.shape[0])
    
    # Create window with extra height for button
    window = pygame.display.set_mode((square_size * game.maze.shape[1], 
                                    square_size * game.maze.shape[0] + 50))
    
    # Button parameters
    button_width = 120
    button_height = 40
    button_x = (square_size * game.maze.shape[1] - button_width) // 2
    button_y = square_size * game.maze.shape[0] + 5
    button_pos = (button_x, button_y)
    button_size = (button_width, button_height)
    
    def reset_display():
        window.fill(background_color)
        draw_maze(window, game.maze, square_size, maze_color)
        #draw_button(window, "New Maze", button_pos, button_size, button_color)
        
    
    # Draw the exit (end point) in blue
        pygame.draw.rect(window, exit_color, 
                     (game.exit[1] * square_size, game.exit[0] * square_size, square_size, square_size))

        pygame.display.update()
    
    reset_display()
    game.print_maze()
    
    show_gen(0, algo, game)
    show_path(window, game, algo.pop[0], square_size, show_path_color)
    
    running = True
    solving = True
    t0 = time.time()
    gen = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEMOTION:
                if is_point_inside_button(event.pos, button_pos, button_size):
                    draw_button(window, "New Maze", button_pos, button_size, button_hover_color)
                else:
                    draw_button(window, "New Maze", button_pos, button_size, button_color)
            elif event.type == MOUSEBUTTONDOWN:
                if is_point_inside_button(event.pos, button_pos, button_size):
                    game, algo = init_game()
                    reset_display()
                    show_gen(0, algo, game)
                    show_path(window, game, algo.pop[0], square_size, show_path_color)
                    solving = True
                    gen = 0
                    t0 = time.time()
        
        if solving:
            best_sample = algo.pop[0]
            if manh_dist(best_sample.end_position, game.exit) == 0:
                print("Maze solved!")
                solving = False
            else:
                gen += 1
                if gen < number_of_generations:
                    algo.do_gen()
                    clear_maze(window, game.maze, square_size, background_color)
                    show_path(window, game, algo.pop[0], square_size, show_path_color)
                    show_gen(gen, algo, game, time=time.time() - t0)
                else:
                    print("Max generations reached!")
                    solving = False
    pygame.quit()

if __name__ == "__main__":
    main()
