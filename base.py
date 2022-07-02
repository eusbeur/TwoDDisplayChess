import os

import moderngl_window as mglw
from BoardManager import Board

class Base(mglw.WindowConfig):
    gl_version = (4, 3)
    title = "ModernGL Example"
    window_size = (920, 920)
    aspect_ratio = 1
    resizable = True
    samples = 16
    

    resource_dir = os.path.normpath(os.path.join(__file__, '../data'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mouse_poz = [0,0]
        self.Board = Board()
    @classmethod
    def run(cls):
        mglw.run_window_config(cls)
    
