import numpy as np
from FigureImport import Figure

class Board:
    
    def __init__(self):
        # position coordinates on board
        self.positions = np.zeros((8,8,2))
        self.initPositions()
        # contains all remaining figures
        self.figures = dict({})
        # translate figure
    
    # set board coords which depend on the png (adjust here)
    def initPositions(self):
        x_0 = -0.8193
        x_1 = 1.0464
        y_0 = -0.8208
        y_1 = 1.0506
        for i in range(8):
            for j in range(8):
                self.positions[i][j] = np.array([x_0 + i*(x_1-x_0)/8, y_0 + j*(y_1-y_0)/8])
    
    # give board coords of the closest boardposition
    def closest(self, coords):
        dist = 4
        dist_ind = (0,0)
        i=0
        j=0
        for i in range(8):
            for j in range(8):
                d = np.linalg.norm(coords-self.positions[i][j])
                if dist > d:
                    dist = d
                    dist_ind = (i,j)
        return dist_ind, self.positions[dist_ind[0],dist_ind[1]]
    
    # returns index of the closest coords from bag of coords
    def closest_to(self, coords, bag):
        dist = 40
        dist_ind = 0
        i=0
        for i in range(len(bag)):
            d = np.linalg.norm(coords-bag[i])
            if dist > d:
                dist = d
                dist_ind = i
        return dist_ind
    
    # returns all positions of the board, which the figure is able to move to
    def get_figure_moves(self, fig_pos, fig_name):
        list_of_moves = []
        return list_of_moves
    
    def move_legal(self, move):
        legal = False
        return legal
    
    # initialize the figures with starting positions
    def initChessBoard(self):
        self.figures = dict(zip([(0,7), (1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0) ]
        , [Figure('T',0, *self.figure_arg([0,7])), Figure('S',0, *self.figure_arg([1,7])),Figure('L',0, *self.figure_arg([2,7])), Figure('K',0, *self.figure_arg([3,7])),Figure('D',0, *self.figure_arg([4,7])), Figure('L',0, *self.figure_arg([5,7])),Figure('S',0, *self.figure_arg([6,7])), Figure('T',0, *self.figure_arg([7,7])),
           Figure('B',0, *self.figure_arg([0,6])), Figure('B',0, *self.figure_arg([1,6])),Figure('B',0, *self.figure_arg([2,6])), Figure('B',0, *self.figure_arg([3,6])),Figure('B',0, *self.figure_arg([4,6])), Figure('B',0, *self.figure_arg([5,6])),Figure('B',0, *self.figure_arg([6,6])), Figure('B',0, *self.figure_arg([7,6])),
           Figure('B',1, *self.figure_arg([0,1])), Figure('B',1, *self.figure_arg([1,1])),Figure('B',1, *self.figure_arg([2,1])), Figure('B',1, *self.figure_arg([3,1])),Figure('B',1, *self.figure_arg([4,1])), Figure('B',1, *self.figure_arg([5,1])),Figure('B',1, *self.figure_arg([6,1])), Figure('B',1, *self.figure_arg([7,1])),
           Figure('T',1, *self.figure_arg([0,0])), Figure('S',1, *self.figure_arg([1,0])),Figure('L',1, *self.figure_arg([2,0])), Figure('K',1, *self.figure_arg([3,0])),Figure('D',1, *self.figure_arg([4,0])), Figure('L',1, *self.figure_arg([5,0])),Figure('S',1, *self.figure_arg([6,0])), Figure('T',1, *self.figure_arg([7,0])),]))
    # arguments for Figure to set the pos and coords at once
    def figure_arg(self, pos):
        coords = self.positions[pos[0]][pos[1]]
        return (pos, coords)
    
class BoardManager:
    
    def __init__(self):
        self.mat = np.zeros((8,8),dtype=np.short)
        self.type_to_short = dict({
            'Kw' : 11,
            'Dw' : 10,
            'Tw' : 9,
            'Lw' : 8,
            'Sw' : 7,
            'Bw' : 6,
            'Ks' : 5,
            'Ds' : 4,
            'Ts' : 3,
            'Ls' : 2,
            'Ss' : 1,
            'Bs' : 0
        })
        self.short_to_type = dict({
            11 : 'Kw',
            10 : 'Dw',
            9 : 'Tw',
            8 : 'Lw',
            7 : 'Sw',
            6 : 'Bw',
            5 : 'Ks',
            4 : 'Ds',
            3 : 'Ts',
            2 : 'Ls',
            1 : 'Ss',
            0 : 'Bs'
        })
        
    def init_from_Board(self, figures: dict):
        for t, fig in figures.items():
            self.mat[t[0]][t[1]] = self.type_to_short[fig.figure + ('w' if fig.color == 1 else 's')]
    
    def get_fig_moves(self, pos):
        destinations = []
        name = self.short_to_char[self.mat[pos[0]][pos[1]][0]]
        color = 0
        if name[1] == 's':
            color = 1
            
        if  name[0] == 'K':
            destinations = self.king_moves(pos)
        elif self.mat[pos[0]][pos[1]][0] == 'D':
            destinations = self.iterate_diagonals(pos) + self. iterate_straight(pos)
        elif self.mat[pos[0]][pos[1]][0] == 'T':
            destinations = self.iterate_straight(pos)
        elif self.mat[pos[0]][pos[1]][0] == 'L':
            destinations = self.iterate_diagonals(pos)
        elif self.mat[pos[0]][pos[1]][0] == 'S':
            destinations = self.iterate_knight(pos)
        elif self.mat[pos[0]][pos[1]][0] == 'B':
            destinations = self.pawn_moves(pos, color)
        return destinations
    
    ## Fig_moves for every type of figure 
    def iterate_diagonals(self, pos):
        minuslim = np.min(pos[0],pos[1])
        pluslim = np.min(7-pos[0],7-pos[1])
        moves = []
        x = pos[0]
        y = pos[1]
        for i in range(minuslim):
            x -= 1
            y -= 1
            moves.append((x,y))
    
        x = pos[0]
        y = pos[1]
        for i in range(pluslim):
            x += 1
            y += 1
            moves.append((x,y))
        minuslim = np.min(pos[0],7-pos[1])
        pluslim = np.min(7-pos[0],pos[1])
        moves = []
        x = pos[0]
        y = pos[1]
        for i in range(minuslim):
            x -= 1
            y += 1
            moves.append((x,y))
    
        x = pos[0]
        y = pos[1]
        for i in range(pluslim):
            x += 1
            y -= 1
            moves.append((x,y))
        return moves
    
    def iterate_straight(self, pos):
        moves = []
        x = pos[0]
        y = pos[1]
        for i in range(x):
            x -= 1
            moves.append((x,y))
        x = pos[0]
        y = pos[1]
        for i in range(y):
            y -= 1
            moves.append((x,y))
        x = pos[0]
        y = pos[1]
        for i in range(7-x):
            x += 1
            moves.append((x,y))
        x = pos[0]
        y = pos[1]
        for i in range(7-x):
            x += 1
            moves.append((x,y))
        return moves
        
    def iterate_knight(self,pos):
        moves = []
        for i in range(2):
            for j in range(2):
                dest = (pos[0]+(-1)**j, pos[1]+2*(-1)**i)
                if dest[0] < 0 or dest[0] > 7:
                    continue
                if dest[1] < 0 or dest[1] > 7:
                    continue
                moves.append(dest)
        for i in range(2):
            for j in range(2):
                dest = (pos[0]+2*(-1)**j, pos[1]+(-1)**i)
                if dest[0] < 0 or dest[0] > 7:
                    continue
                if dest[1] < 0 or dest[1] > 7:
                    continue
                moves.append(dest)
        return moves
    
    def pawn_moves(self, pos, color):
        moves = []
        if color == 0:
            if pos[1] == 1:
                pass
        return moves
    
    def king_moves(self, pos):
        moves = []
        return moves
        