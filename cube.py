from vpython import *
import numpy as np
import random
import kociemba

def proximity(pos, target):
    delta = 0.2
    result = False
    if pos.x + delta > target[0] and pos.x - delta < target[0]:
        if pos.y + delta > target[1] and pos.y - delta < target[1]:
            if pos.z + delta > target[2] and pos.z - delta < target[2]:
                result = True
    return result

def color_detect(color_value):
    value = (color_value.x, color_value.y, color_value.z)
    color_result = None
    if value == (1,0,0):
        color_result = 'F'
    elif value == (1,1,0):
        color_result = 'R'
    elif value == (1, 0.5, 0):
        color_result = 'B'
    elif value == (1, 1, 1):
        color_result = 'L'
    elif value == (0, 0, 1):
        color_result = 'U'
    elif value == (0, 1, 0):
        color_result = 'D'
    return color_result

def decode_postion(cube):
    '''F = red, R = yellow, B = orange, L = white, U = blue, D = green'''
    value = ['0']*54
    positions = [
        ((-1,1.5,-1), 0), (0,1.5,-1, 1), (1,1.5,-1, 2),  # U1-U3
        ((-1,1.5,0), 3), (0,1.5,0, 4), (1,1.5,0, 5),     # U4-U6
        ((-1,1.5,1), 6), (0,1.5,1, 7), (1,1.5,1, 8),     # U7-U9
        # ... rest of the positions mapping
    ]

    for tile in cube:
        if proximity(tile.pos,(-1,1.5,-1)): #U1
            value[0] = color_detect(tile.color)
    
    for tile in cube:
        if proximity(tile.pos,(-1,1.5,-1)): #U1
            value[0] = color_detect(tile.color)
        elif proximity(tile.pos,(0,1.5,-1)): #U2
            value[1] = color_detect(tile.color)
        elif proximity(tile.pos,(1,1.5,-1)): #U3
            value[2] = color_detect(tile.color)
        elif proximity(tile.pos,(-1,1.5,0)): #U4
            value[3] = color_detect(tile.color)
        elif proximity(tile.pos,(0,1.5,0)): #U5
            value[4] = color_detect(tile.color)
        elif proximity(tile.pos,(1,1.5,0)): #U6
            value[5] = color_detect(tile.color)
        elif proximity(tile.pos,(-1,1.5,1)): #U7
            value[6] = color_detect(tile.color)
        elif proximity(tile.pos,(0,1.5,1)): #U8
            value[7] = color_detect(tile.color)
        elif proximity(tile.pos,(1,1.5,1)): #U9
            value[8] = color_detect(tile.color)
        elif proximity(tile.pos,(1.5,1,1)): #R1
            value[9] = color_detect(tile.color)
        elif proximity(tile.pos,(1.5,1,0)): #R2
            value[10] = color_detect(tile.color)
        elif proximity(tile.pos,(1.5,1,-1)): #R3
            value[11] = color_detect(tile.color)
        elif proximity(tile.pos,(1.5,0,1)): #R4
            value[12] = color_detect(tile.color)
        elif proximity(tile.pos,(1.5,0,0)): #R5
            value[13] = color_detect(tile.color)
        elif proximity(tile.pos,(1.5,0,-1)): #R6
            value[14] = color_detect(tile.color)
        elif proximity(tile.pos,(1.5,-1,1)): #R7
            value[15] = color_detect(tile.color)
        elif proximity(tile.pos,(1.5,-1,0)): #R8
            value[16] = color_detect(tile.color)
        elif proximity(tile.pos,(1.5,-1,-1)): #R9
            value[17] = color_detect(tile.color)
        elif proximity(tile.pos,(-1,1,1.5)): #F1
            value[18] = color_detect(tile.color)
        elif proximity(tile.pos,(0,1,1.5)): #F2
            value[19] = color_detect(tile.color)
        elif proximity(tile.pos,(1,1,1.5)): #F3
            value[20] = color_detect(tile.color)
        elif proximity(tile.pos,(-1,0,1.5)): #F4
            value[21] = color_detect(tile.color)
        elif proximity(tile.pos,(0,0,1.5)): #F5
            value[22] = color_detect(tile.color)
        elif proximity(tile.pos,(1,0,1.5)): #F6
            value[23] = color_detect(tile.color)
        elif proximity(tile.pos,(-1,-1,1.5)): #F7
            value[24] = color_detect(tile.color)
        elif proximity(tile.pos,(0,-1,1.5)): #F8
            value[25] = color_detect(tile.color)
        elif proximity(tile.pos,(1,-1,1.5)): #F9
            value[26] = color_detect(tile.color)
        elif proximity(tile.pos,(-1,-1.5,1)): #D1
            value[27] = color_detect(tile.color)
        elif proximity(tile.pos,(0,-1.5,1)): #D2
            value[28] = color_detect(tile.color)
        elif proximity(tile.pos,(1,-1.5,1)): #D3
            value[29] = color_detect(tile.color)
        elif proximity(tile.pos,(-1,-1.5,0)): #D4
            value[30] = color_detect(tile.color)
        elif proximity(tile.pos,(0,-1.5,0)): #D5
            value[31] = color_detect(tile.color)
        elif proximity(tile.pos,(1,-1.5,0)): #D6
            value[32] = color_detect(tile.color)
        elif proximity(tile.pos,(-1,-1.5,-1)): #D7
            value[33] = color_detect(tile.color)
        elif proximity(tile.pos,(0,-1.5,-1)): #D8
            value[34] = color_detect(tile.color)
        elif proximity(tile.pos,(1,-1.5,-1)): #D9
            value[35] = color_detect(tile.color)
        elif proximity(tile.pos,(-1.5,1,-1)): #L1
            value[36] = color_detect(tile.color)
        elif proximity(tile.pos,(-1.5,1,0)): #L2
            value[37] = color_detect(tile.color)
        elif proximity(tile.pos,(-1.5,1,1)): #L3
            value[38] = color_detect(tile.color)
        elif proximity(tile.pos,(-1.5,0,-1)): #L4
            value[39] = color_detect(tile.color)
        elif proximity(tile.pos,(-1.5,0,0)): #L5
            value[40] = color_detect(tile.color)
        elif proximity(tile.pos,(-1.5,0,1)): #L6
            value[41] = color_detect(tile.color)
        elif proximity(tile.pos,(-1.5,-1,-1)): #L7
            value[42] = color_detect(tile.color)
        elif proximity(tile.pos,(-1.5,-1,0)): #L8
            value[43] = color_detect(tile.color)
        elif proximity(tile.pos,(-1.5,-1,1)): #L9
            value[44] = color_detect(tile.color)
        elif proximity(tile.pos,(1,1,-1.5)): #B1
            value[45] = color_detect(tile.color)
        elif proximity(tile.pos,(0,1,-1.5)): #B2
            value[46] = color_detect(tile.color)
        elif proximity(tile.pos,(-1,1,-1.5)): #B3
            value[47] = color_detect(tile.color)
        elif proximity(tile.pos,(1,0,-1.5)): #B4
            value[48] = color_detect(tile.color)
        elif proximity(tile.pos,(0,0,-1.5)): #B5
            value[49] = color_detect(tile.color)
        elif proximity(tile.pos,(-1,0,-1.5)): #B6
            value[50] = color_detect(tile.color)
        elif proximity(tile.pos,(1,-1,-1.5)): #B7
            value[51] = color_detect(tile.color)
        elif proximity(tile.pos,(0,-1,-1.5)): #B8
            value[52] = color_detect(tile.color)
        elif proximity(tile.pos,(-1,-1,-1.5)): #B9
            value[53] = color_detect(tile.color)
    return value

def solve(cube):
    values = ""
    values = values.join(decode_postion(cube))
    solution = kociemba.solve(values)
    print('solution is \n' + solution)
    return solution

class Rubik_Cube():
    def __init__(self):
        # Set up the scene with better positioning and camera
        scene.width = 2000  # Increased width
        scene.height = 600
        scene.background = color.white
        scene.camera.pos = vector(5, 3, 5)
        scene.camera.axis = vector(-5, -3, -5)
        # Center-align the caption
        scene.caption = """<div style='text-align:center;'>
            <div style='margin: 10px 0;'><b>Cube Controls</b></div>
        </div>"""
        
        self.running = True
        self.tiles = []
        self.dA = np.pi/40
        
        # Center black core with slightly larger size for better visibility
        sphere(pos=vector(0,0,0), size=vector(2.9,2.9,2.9), color=vector(0.1,0.1,0.1))
        
        # [Rest of the initialization code remains unchanged]
        tile_pos = [
            [vector(-1, 1, 1.5),vector(0, 1, 1.5),vector(1, 1, 1.5),           
             vector(-1, 0, 1.5),vector(0, 0, 1.5),vector(1, 0, 1.5),
             vector(-1, -1, 1.5),vector(0, -1, 1.5),vector(1, -1, 1.5), ],
            [vector(1.5, 1, -1), vector(1.5, 1, 0), vector(1.5, 1, 1),         
             vector(1.5, 0, -1), vector(1.5, 0, 0), vector(1.5, 0, 1),
             vector(1.5, -1, -1), vector(1.5, -1, 0), vector(1.5, -1, 1), ],
            [vector(-1, 1, -1.5), vector(0, 1, -1.5), vector(1, 1, -1.5),      
             vector(-1, 0, -1.5), vector(0, 0, -1.5), vector(1, 0, -1.5),
             vector(-1, -1, -1.5), vector(0, -1, -1.5), vector(1, -1, -1.5), ],
            [vector(-1.5, 1, -1), vector(-1.5, 1, 0), vector(-1.5, 1, 1),      
             vector(-1.5, 0, -1), vector(-1.5, 0, 0), vector(-1.5, 0, 1),
             vector(-1.5, -1, -1), vector(-1.5, -1, 0), vector(-1.5, -1, 1), ],
            [vector(-1, 1.5, -1), vector(0, 1.5, -1), vector(1, 1.5, -1),      
             vector(-1, 1.5, 0), vector(0, 1.5, 0), vector(1, 1.5, 0),
             vector(-1, 1.5, 1), vector(0, 1.5, 1), vector(1, 1.5, 1), ],
            [vector(-1, -1.5, -1), vector(0, -1.5, -1), vector(1, -1.5, -1),   
             vector(-1, -1.5, 0), vector(0, -1.5, 0), vector(1, -1.5, 0),
             vector(-1, -1.5, 1), vector(0, -1.5, 1), vector(1, -1.5, 1), ],
        ]
        
        colors = [vector(1,0,0),vector(1,1,0),vector(1,0.5,0),vector(1,1,1),vector(0,0,1),vector(0,1,0)]
        angle = [(0,vector(0,0,0)),(np.pi/2,vector(0,1,0)),(0,vector(0,0,0)),(np.pi/2,vector(0,1,0)),(np.pi/2,vector(1,0,0)),(np.pi/2,vector(1,0,0))]
        
        # Create tiles with slightly larger gaps between them
        for rank,side in enumerate(tile_pos):
            for vec in side:
                tile = box(pos=vec, size=vector(0.95,0.95,0.1), color=colors[rank])
                tile.rotate(angle=angle[rank][0], axis=angle[rank][1])
                self.tiles.append(tile)
        
        self.positions = {'front':[],'right':[],'back':[],'left':[],'top':[],'bottom':[]}
        self.rotate = [None,0,0]
        self.moves = []

    def reset_positions(self):
        self.positions = {'front': [], 'right': [], 'back': [], 'left': [], 'top': [], 'bottom': []}
        for tile in self.tiles:
            if tile.pos.z > 0.4:
                self.positions['front'].append(tile)
            if tile.pos.x > 0.4:
                self.positions['right'].append(tile)
            if tile.pos.z < -0.4:
                self.positions['back'].append(tile)
            if tile.pos.x < -0.4:
                self.positions['left'].append(tile)
            if tile.pos.y > 0.4:
                self.positions['top'].append(tile)
            if tile.pos.y < -0.4:
                self.positions['bottom'].append(tile)
        for key in self.positions.keys():
            self.positions[key] = set(self.positions[key])

    def animations(self):
        if self.rotate[0] == 'front_counter':
            pieces = self.positions['front']
            for tile in pieces:
                tile.rotate(angle=(self.dA),axis = vector(0,0,1),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'right_counter':
            pieces = self.positions['right']
            for tile in pieces:
                tile.rotate(angle=(self.dA),axis = vector(1,0,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'back_counter':
            pieces = self.positions['back']
            for tile in pieces:
                tile.rotate(angle=(self.dA),axis = vector(0,0,-1),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'left_counter':
            pieces = self.positions['left']
            for tile in pieces:
                tile.rotate(angle=(self.dA),axis = vector(-1,0,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'top_counter':
            pieces = self.positions['top']
            for tile in pieces:
                tile.rotate(angle=(self.dA),axis = vector(0,1,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'bottom_counter':
            pieces = self.positions['bottom']
            for tile in pieces:
                tile.rotate(angle=(self.dA),axis = vector(0,-1,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'front_clock':
            pieces = self.positions['front']
            for tile in pieces:
                tile.rotate(angle=(-self.dA),axis = vector(0,0,1),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'right_clock':
            pieces = self.positions['right']
            for tile in pieces:
                tile.rotate(angle=(-self.dA),axis = vector(1,0,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'back_clock':
            pieces = self.positions['back']
            for tile in pieces:
                tile.rotate(angle=(-self.dA),axis = vector(0,0,-1),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'left_clock':
            pieces = self.positions['left']
            for tile in pieces:
                tile.rotate(angle=(-self.dA),axis = vector(-1,0,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'top_clock':
            pieces = self.positions['top']
            for tile in pieces:
                tile.rotate(angle=(-self.dA),axis = vector(0,1,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        elif self.rotate[0] == 'bottom_clock':
            pieces = self.positions['bottom']
            for tile in pieces:
                tile.rotate(angle=(-self.dA),axis = vector(0,-1,0),origin=vector(0,0,0))
            self.rotate[1] += self.dA
        if self.rotate[1] + self.dA/2 > self.rotate[2] and \
            self.rotate[1] - self.dA/2 < self.rotate[2]:
            self.rotate = [None,0,0]
            self.reset_positions()

    def rotate_front_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['front_counter',0,np.pi/2]

    def rotate_right_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['right_counter',0,np.pi/2]

    def rotate_back_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['back_counter',0,np.pi/2]

    def rotate_left_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['left_counter',0,np.pi/2]

    def rotate_top_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['top_counter',0,np.pi/2]

    def rotate_bottom_counter(self):
        if self.rotate[0] == None:
            self.rotate = ['bottom_counter',0,np.pi/2]

    def rotate_front_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['front_clock',0,np.pi/2]

    def rotate_right_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['right_clock',0,np.pi/2]

    def rotate_back_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['back_clock',0,np.pi/2]

    def rotate_left_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['left_clock',0,np.pi/2]

    def rotate_top_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['top_clock',0,np.pi/2]

    def rotate_bottom_clock(self):
        if self.rotate[0] == None:
            self.rotate = ['bottom_clock',0,np.pi/2]

    def move(self):
        possible_moves = ["F", "R", "B", "L", "U", "D", "F'", "R'", "B'", "L'", "U'", "D'"]
        if self.rotate[0] == None and len(self.moves) > 0:
            if self.moves[0] == possible_moves[0]:
                self.rotate_front_clock()
            elif self.moves[0] == possible_moves[1]:
                self.rotate_right_clock()
            elif self.moves[0] == possible_moves[2]:
                self.rotate_back_clock()
            elif self.moves[0] == possible_moves[3]:
                self.rotate_left_clock()
            elif self.moves[0] == possible_moves[4]:
                self.rotate_top_clock()
            elif self.moves[0] == possible_moves[5]:
                self.rotate_bottom_clock()
            elif self.moves[0] == possible_moves[6]:
                self.rotate_front_counter()
            elif self.moves[0] == possible_moves[7]:
                self.rotate_right_counter()
            elif self.moves[0] == possible_moves[8]:
                self.rotate_back_counter()
            elif self.moves[0] == possible_moves[9]:
                self.rotate_left_counter()
            elif self.moves[0] == possible_moves[10]:
                self.rotate_top_counter()
            elif self.moves[0] == possible_moves[11]:
                self.rotate_bottom_counter()
            self.moves.pop(0)

    def scramble(self):
        possible_moves = ["F","R","B","L","U","D","F'","R'","B'","L'","U'","D'"]
        for i in range(25):
            self.moves.append(random.choice(possible_moves))

    def solution(self):
        solve(self.tiles)

    def solve(self):
        values = solve(self.tiles)
        values = list(values.split(" "))
        for value in values:
            lis_value = list(value)
            if lis_value[-1] == '2':
                lis_value.pop(-1)
                value = ''.join(lis_value)
                self.moves.append(value)
                self.moves.append(value)
            else:
                self.moves.append(value)

    def control(self):
     scene.append_to_caption("<div style='text-align: center; white-space: nowrap;'>")
    
    # Rotation buttons
     button(bind=self.rotate_front_clock, text='F', background=color.red)
     button(bind=self.rotate_front_counter, text="F'", background=color.red)
     button(bind=self.rotate_right_clock, text='R', background=color.yellow)
     button(bind=self.rotate_right_counter, text="R'", background=color.yellow)
     button(bind=self.rotate_back_clock, text='B', background=color.orange)
     button(bind=self.rotate_back_counter, text="B'", background=color.orange)
     button(bind=self.rotate_left_clock, text='L', background=color.white)
     button(bind=self.rotate_left_counter, text="L'", background=color.white)
     button(bind=self.rotate_top_clock, text='U', background=color.blue)
     button(bind=self.rotate_top_counter, text="U'", background=color.blue)
     button(bind=self.rotate_bottom_clock, text='D', background=color.green)
     button(bind=self.rotate_bottom_counter, text="D'", background=color.green)

    # Action buttons
     button(bind=self.scramble, text='Scramble', background=color.yellow)
     button(bind=self.solution, text='Show Solution', background=color.cyan)
     button(bind=self.solve, text='Solve!', background=color.green)
    
    scene.append_to_caption("</div>")
    def update(self):
        rate(60)
        self.animations()
        self.move()

    def start(self):
        self.reset_positions()
        self.control()
        while self.running:
            self.update()

if __name__ == "__main__":
    cube = Rubik_Cube()
    cube.start()