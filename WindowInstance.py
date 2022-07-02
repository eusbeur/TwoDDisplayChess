"""
Instanced rendering without supplying per instance data
doing offsets with gl_InstanceID in vertex shader.
"""
import numpy as np

import moderngl
from base import Base


class InstancedRendering(Base):
    title = "Instanced Rendering"
    gl_version = (4, 3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # gl_InstanceID offsets rotation per instance
        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330

                in vec2 in_vert;
                in vec4 in_color;

                out vec4 v_color;

                uniform float Rotation;
                uniform vec2 Scale;

                void main() {
                    v_color = in_color;
                    float r = Rotation * (0.5 + gl_InstanceID * 0.05);
                    mat2 rot = mat2(cos(r), sin(r), -sin(r), cos(r));
                    gl_Position = vec4((rot * in_vert) * Scale, 0.0, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                in vec4 v_color;
                out vec4 f_color;

                void main() {
                    f_color = v_color;
                }
            ''',
        )

        self.scale = self.prog['Scale']
        self.rotation = self.prog['Rotation']

        vertices = np.array([
            # x, y, red, green, blue, alpha
            1.0, 0.0, 1.0, 0.0, 0.0, 0.5,
            -0.5, 0.86, 0.0, 1.0, 0.0, 0.5,
            -0.5, -0.86, 0.0, 0.0, 1.0, 0.5,
        ], dtype='f4')

        self.vbo = self.ctx.buffer(vertices)
        self.vao = self.ctx.vertex_array(
            self.prog,
            [(self.vbo, '2f 4f', 'in_vert', 'in_color')],
        )

    def render(self, time, frame_time):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.BLEND)
        self.scale.value = (0.5, self.aspect_ratio * 0.5)
        self.rotation.value = time
        # For every instanced rendered gl_InstanceID increments by 1
        self.vao.render(instances=10)

class Fractal(Base):
    title = "Julia Set"
    gl_version = (4, 3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330

                in vec2 in_vert;
                out vec2 v_text;

                void main() {
                    gl_Position = vec4(in_vert*1000, 0.0, 1.0);
                    v_text = in_vert;
                }
            ''',
            fragment_shader='''
                #version 330

                in vec2 v_text;
                out vec4 f_color;

                uniform sampler2D Texture;
                uniform vec2 Seed;
                uniform int Iter;

                void main() {
                    vec2 c = Seed;
                    int i;

                    vec2 z = vec2(3.0 * v_text.x, 2.0 * v_text.y);

                    for (i = 0; i < Iter; i++) {
                        float x = (z.x * z.x - z.y * z.y) + c.x;
                        float y = 2*(z.x * z.y) + c.y;

                        if ((x * x + y * y) > 4.0) {
                            break;
                        }
                        z.x = x;
                        z.y = y;
                    }

                    f_color = texture(Texture, vec2((i == Iter ? 0.0 : float(i+1))/800.0, float(i)/1000));
                }
            ''',
        )

        self.seed = self.prog['Seed']
        self.iter = self.prog['Iter']

        self.texture = self.load_texture_2d('color.jpg')

        vertices = np.array([-1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0])

        self.vbo = self.ctx.buffer(vertices.astype('f4'))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert')
        self.texture.anisotropy = 16.0

    def render(self, time, frame_time):
        self.ctx.clear(1.0, 1.0, 1.0)

        self.seed.value = (-0.8, 0.156)
        self.iter.value = 10000

        self.texture.use()
        self.vao.render(moderngl.TRIANGLE_STRIP)

if __name__ == '__main__':
    Fractal.run()
