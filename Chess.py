"""
Instanced rendering without supplying per instance data
doing offsets with gl_InstanceID in vertex shader.
"""
import numpy as np

import moderngl
from trimesh import PointCloud
from FigureImport import Figure
from base import Base

from PIL import Image as img
from PIL import ImageOps as imgo

class Chess(Base):
    title = "Schach"
    gl_version = (4, 3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 430

                in vec3 in_vert;
                out vec3 v_text;

                void main() {
                    gl_Position = vec4(in_vert, 1);
                    v_text = in_vert;
                }
            ''',
            fragment_shader='''
                #version 430

                in vec3 v_text;
                out vec4 f_color;

                uniform sampler2D textureBoard;
                //uniform vec2 Seed;
                //uniform int Iter;

                void main() {
                    f_color = texture(textureBoard, vec2(v_text.x,v_text.y)/2.0 + vec2(0.5,0.5))/2.0;
                }
            ''',
        )

        self.prog2 = self.ctx.program(
            vertex_shader= """
            #version 430

                in vec3 in_vert;
                in vec2 in_text;
                out vec2 v_text;

                void main() {
                    gl_Position = vec4(in_vert, 1);
                    v_text = in_text;
                }
            """
            , fragment_shader='''
                #version 430

                in vec2 v_text;
                out vec4 f_color;

                uniform ivec2 T;
                uniform sampler2D textureFigures;
                //uniform vec2 Seed;
                //uniform int Iter;

                void main() {

                    f_color = texture(textureFigures, v_text + vec2(0.5,0.5) + T);

                }
            ''' 
        )
        
        #self.seed = self.prog['Seed']
        #self.iter = self.prog['Iter']
        #self.figure_text_size = self.prog2['T']
        self.prog['textureBoard'] = 0
        self.prog2['textureFigures'] = 1

        data = img.open('data/chess_board.png').convert('RGBA')
        data = imgo.flip(data)
        self.texture = self.ctx.texture(data.size, 4, data.tobytes())
        print(data.size)
        
        self.Board.initChessBoard()
        self.active_figure = list(self.Board.figures.values())[0]

        self.figure_textures = []
        self.chess_canvas = np.array([-1.0, -1.0, 1.0, -1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0])
        for fig in self.Board.figures.values():
            self.figure_textures.append(self.ctx.texture(fig.data.size, 4, fig.data.tobytes()))
            self.figure_textures[-1].use(location=1)
            
        self.texture.use(location=0)

        self.vbo = self.ctx.buffer(self.chess_canvas.astype('f4'))
        self.vbo_figures = self.ctx.buffer(self.active_figure.get_vertices(0.5).astype('f4'))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert')
        self.vao_figures = self.ctx.simple_vertex_array(self.prog2, self.vbo_figures, 'in_vert', 'in_text')

    # render background board texture and figures
    def render(self, time, frame_time):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.BLEND)
        #self.vbo.orphan()
        #self.vbo.write(self.chess_canvas.astype('f4'))
        self.texture.use(location=0)
        self.vao.render(moderngl.TRIANGLE_STRIP)
        #self.vbo.orphan()

        for i, fig in zip(range(len(self.Board.figures.values())),self.Board.figures.values()):
            self.vbo_figures.orphan()
            self.vbo_figures.write(fig.get_vertices(0.5).astype('f4'))
            self.figure_textures[i].use(location=1)
            self.vao_figures.render(moderngl.TRIANGLE_STRIP)
            #print(fig.pos, fig.coords)


    def mouse_press_event(self, x: int, y: int, button: int):
        figure_positions = []
        for i in range(len(self.Board.figures.values())):
            pos = list(self.Board.figures.values())[i].coords
            figure_positions.append(pos)
            
        n = self.Board.closest_to(self.mouse_poz, figure_positions)
        self.active_figure = list(self.Board.figures.values())[n]
        #return super().mouse_press_event(x, y, button)
    
    def mouse_drag_event(self, x: int, y: int, dx: int, dy: int):
        w = np.min(self.window_size)
        self.mouse_poz = [x*2/w-1,-y*2/w+1]
        self.active_figure.set_coords(self.mouse_poz)
        #return super().mouse_drag_event(x, y, dx, dy)
    
    def mouse_release_event(self, x: int, y: int, button: int):
        self.active_figure.set_coord_state(*self.Board.closest(self.mouse_poz))
        #return super().mouse_release_event(x, y, button)
    
    def mouse_position_event(self, x, y, dx, dy):
        w = np.min(self.window_size)
        self.mouse_poz = [x*2/w-1,-y*2/w+1]
        #print("Mouse position", self.mouse_poz)
    

    
if __name__ == '__main__':
    Chess.run()