import tkinter as tk
import subprocess
import sys

class GameLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Evolutionary Puzzle Solver")
        self.root.geometry("1000x800")
        
        # Define aesthetic colors with Coral Grey
        self.colors = {
            'bg_gradient_start': '#6A4E23',  # Umber (Deep brownish-red)
            'bg_gradient_end': '#D0C3B2',  # White Coffee (Warm beige)
            'text': '#3E2723',  # Ebony Clay (Sophisticated dark gray with brownish tint)
            'card_bg': '#A99A8D',  # Coral Grey (Soft muted coral with greyish tint)
            'button_border': '#3E2723',  # Ebony Clay (Darker button borders)
            'button_hover': '#FFEB3B',  # Confetti (Bright playful yellow for hover effect)
            'button_active': '#A1887F',  # Khaki (Active button color)
            'shadow': '#3E2723',  # Ebony Clay (Dark shadow for buttons and cards)
            'dark_green': '#2C6E49',  # Dark Green (Deep and calming green)
            'morning_blue': '#7F9E8E',  # Morning Blue (Soft calming blue)
            'fountain_blue': '#A7D8F7',  # Fountain Blue (Light blue)
            'astronaut': '#2F3B56',  # Astronaut (Rich dark blue)
            'light_coral': '#F08080',  # Light Coral (Warm coral)
            'grey': '#B0B0B0'  # Soft neutral grey
        }
        
        # Animation parameters
        self.glow_steps = 10
        self.glow_delay = 20
        self.active_animations = {}
        
        # Configure the main window
        self.root.configure(bg=self.colors['bg_gradient_end'])
        
        # Create main container
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg_gradient_end'], padx=50, pady=50)
        self.main_frame.pack(expand=True, fill='both')
        
        # Title with elegant font
        title = tk.Label(self.main_frame, text="Evolutionary Puzzle Solver", font=('Helvetica', 48, 'bold'), fg=self.colors['text'], bg=self.colors['bg_gradient_end'])
        title.pack(pady=(0, 30))
        
        # Create game container
        self.game_container = tk.Frame(self.main_frame, bg=self.colors['bg_gradient_end'])
        self.game_container.pack(expand=True, fill='both')
        
        # Configure grid columns for better layout handling
        for i in range(5):  # Adjusted for more game cards
            self.game_container.grid_columnconfigure(i, weight=1)
        
        # Create game cards
        self.create_game_cards()
        
        # Create chatbot button
        self.create_chatbot_button()

    def interpolate_color(self, start_color, end_color, fraction):
        """Interpolate between two colors"""
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        
        start_rgb = hex_to_rgb(start_color)
        end_rgb = hex_to_rgb(end_color)
        
        current_rgb = tuple(
            start + (end - start) * fraction
            for start, end in zip(start_rgb, end_rgb)
        )
        
        return rgb_to_hex(current_rgb)

    def animate_glow(self, button, entering):
        """Animate the button glow effect"""
        widget_id = str(button)
        
        if widget_id in self.active_animations:
            self.root.after_cancel(self.active_animations[widget_id])
        
        start_color = self.colors['bg_gradient_end'] if entering else self.colors['button_hover']
        end_color = self.colors['button_hover'] if entering else self.colors['bg_gradient_end']
        
        def animate_step(step):
            if step <= self.glow_steps:
                fraction = step / self.glow_steps
                current_color = self.interpolate_color(start_color, end_color, fraction)
                button.configure(bg=current_color)
                self.active_animations[widget_id] = self.root.after(
                    self.glow_delay, 
                    lambda: animate_step(step + 1)
                )
            else:
                if widget_id in self.active_animations:
                    del self.active_animations[widget_id]
        
        animate_step(0)

    def create_styled_button(self, parent, text, command):
        """Create a button with elegant dark styling"""
        button = tk.Button(
            parent,
            text=text.upper(),
            command=command,
            font=('Helvetica', 14, 'bold'),
            fg=self.colors['text'],  # Soft light gray text
            bg=self.colors['bg_gradient_end'],
            activebackground=self.colors['button_hover'],
            activeforeground=self.colors['text'],
            bd=0,
            relief='flat',
            padx=20,
            pady=12,
            width=15
        )
        button.configure(highlightbackground=self.colors['button_border'])
        
        button.bind('<Enter>', lambda e: self.animate_glow(e.widget, True))
        button.bind('<Leave>', lambda e: self.animate_glow(e.widget, False))
        
        return button

    def create_game_card(self, title, row, col, buttons_config):
        """Create a game card with title and buttons"""
        card = tk.Frame(self.game_container, bg=self.colors['card_bg'], padx=20, pady=20, bd=0, relief='flat')
        card.grid(row=row, column=col, padx=25, pady=25, sticky='nsew')
        
        # Shadow effect using canvas
        card_shadow = tk.Canvas(card, width=250, height=200, bg=self.colors['shadow'], bd=0, highlightthickness=0)
        card_shadow.place(x=10, y=10)
        card_shadow.create_rectangle(10, 10, 250, 200, fill=self.colors['card_bg'], outline="")
        
        # Use dynamic font size based on title length
        font_size = 18 if len(title) <= 10 else 14  # Adjust font size
        tk.Label(
            card,
            text=title,
            font=('Helvetica', font_size, 'bold'),
            fg=self.colors['text'],  # Light gray text
            bg=self.colors['card_bg'],
            wraplength=150  # Ensure long titles wrap if needed
        ).pack(pady=(0, 15))
        
        for btn_text, command in buttons_config:
            button = self.create_styled_button(card, btn_text, command)
            button.pack(pady=10)

    def create_game_cards(self):
        """Create all game cards"""
        self.create_game_card("Rubik's Cube", 0, 0, [
            ("Solve", self.launch_rubiks_cube)
        ])
        
        self.create_game_card("Sudoku", 0, 1, [
            ("Play", self.launch_sudoku_play),
            ("Solve", self.launch_sudoku_solve)
        ])
        
        self.create_game_card("Maze", 0, 2, [
            ("Play", self.launch_maze_play),
            ("Solve", self.launch_maze_solve)
        ])
        
        self.create_game_card("N-Queen", 0, 3, [
            ("Learn", self.launch_n_queens)
        ])

        self.create_game_card("Tic-Tac-Toe", 0, 4, [
            ("Play", self.launch_tictactoe)
        ])
    
    def create_chatbot_button(self):
        """Create the chatbot button at the bottom"""
        chatbot_frame = tk.Frame(self.main_frame, bg=self.colors['bg_gradient_end'])
        chatbot_frame.pack(pady=30)
        
        chatbot_button = self.create_styled_button(
            chatbot_frame,
            "Chatbot",
            self.launch_chatbot
        )
        chatbot_button.configure(font=('Helvetica', 14, 'bold'))
        chatbot_button.pack()
    
    def run_script(self, script_name):
        """Run a Python script"""
        try:
            subprocess.Popen([sys.executable, script_name])
        except Exception as e:
            print(f"Error launching {script_name}: {e}")
    
    # Launch handlers
    def launch_rubiks_cube(self):
        self.run_script('cube.py')

    def launch_sudoku_play(self):
        self.run_script('sudoku3.py')
        
    def launch_sudoku_solve(self):
        self.run_script('SUDOKOfinal.py')

    def launch_maze_play(self):
        self.run_script('maze_puzzlefinal.py')
        
    def launch_maze_solve(self):
        self.run_script('maze.py')

    def launch_n_queens(self):
        self.run_script('n_queens_solver.py')
    
    def launch_tictactoe(self):
        self.run_script('tictactoe.py')

    def launch_chatbot(self):
        self.run_script('chatbot.py')

    def run(self):
        # Center the window on the screen
        self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_toplevel())
        self.root.mainloop()

# Run the launcher
launcher = GameLauncher()
launcher.run()
