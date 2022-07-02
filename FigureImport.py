from PIL import Image, ImageOps
import numpy as np
#from BoardManager import Board

class Figure:
    
    # does some additional scaling condition
    def __init__(self, figure, color, pos, coords):
        self.data = ImageOps.flip(Image.open('data/chess_figures.png').convert('RGBA'))
        # 0 : white, 1 : black
        self.color = color
        self.figure = figure
        self.scale_factor = 1.0
        self.height_scale = 1.0
        self.height_offset = 0
        self.coords = coords
        self.pos = pos
        self.initial_pos = self.pos
        if self.color == 1:
            self.data = self.data.crop(tuple(self.chooseFigure() + np.array([0,1,0,1])*560))
        else:
            self.data = self.data.crop(tuple(self.chooseFigure()))
        
        if self.figure == 'K':
            self.scale_factor = 1.2
        elif self.figure == 'B':
            self.scale_factor = 0.7
            self.height_offset = -0.022
        elif self.figure == 'S':
            self.scale_factor = 0.9
            self.height_offset = -0.015
        elif self.figure == 'T':
            self.scale_factor = 1.1
        elif self.figure == 'L':
            self.scale_factor = 0.9
            self.height_offset = -0.015
        elif self.figure == 'D':
            self.scale_factor = 0.9
            self.height_scale = 1.4
            self.height_offset = 0.01
    
    # windows in texture which draw the right figure
    def chooseFigure(self):
        switch = dict({
            'K' : np.array([1005,0,1330,470]),
            'D' : np.array([742,0,1028,450]),
            'L' : np.array([570,0,750,400]),
            'S' : np.array([350,0,560,400]),
            'T' : np.array([150,0,348,400]),
            'B' : np.array([0,0,150,300]),
        })
        return switch[self.figure]
    
    # give the vertices of canvas and texture-part in 1D-sequence
    def get_vertices(self, z):
        vertices = []
        m = self.coords
        w = 1/6 * self.scale_factor
        h = 1/6 * self.scale_factor * self.height_scale
        canvas = [m-np.array([w,h])/2,m+np.array([-w,h])/2,m+np.array([w,-h])/2,m+np.array([w,h])/2]
        canvas = [x+np.array([0,self.height_offset]) for x in canvas]
        text = np.array([[0,0], [0,1], [1,0], [1,1]])
        text = [np.array(x) - np.array([0.5,0.5]) for x in text]
            
        for i in range(len(canvas)):
            vertices += list(canvas[i])
            vertices.append(z)
            vertices.append(text[i][0])
            vertices.append(text[i][1])
            
        return np.array(vertices)
    
    # set coords without int pos
    def set_coords(self, m):
        self.coords = m
        
    def set_coord_state(self, pos, coords):
        self.pos = pos
        self.coords = coords
    
    