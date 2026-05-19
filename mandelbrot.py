import pygame as pg
import moderngl as mgl
import numpy as np

WIDTH = 1280
HEIGHT = 720
TITLE = 'Mandelbrot'
FPS = 60

BLACK = (0, 0, 0)


def load_program(ctx: mgl.Context, shader_source: str):
    with open(shader_source) as f:
        source = f.read()
    
    vert_source = ''
    frag_source = ''

    is_vert = True

    for line in source.splitlines():
        if '#begin' in line:
            if 'vertex' in line:
                is_vert = True
            elif 'fragment' in line:
                is_vert = False
        elif is_vert:
            vert_source += line + '\n'
        else:
            frag_source += line + '\n'
    
    return ctx.program(
        vertex_shader=vert_source,
        fragment_shader=frag_source
    )


pg.init()
pg.display.set_caption(TITLE)
screen = pg.display.set_mode((WIDTH, HEIGHT), flags=pg.DOUBLEBUF | pg.OPENGL)
clock = pg.time.Clock()

ctx = mgl.create_context()
program = load_program(ctx, 'shader.glsl')
indices = np.array([
    0, 1, 2,
    1, 2, 3,
], dtype=np.uint32)
vertices = np.array([
    -1.0,  1.0, # Top left
     1.0,  1.0, # Top right
    -1.0, -1.0, # Bottom left
     1.0, -1.0, # Bottom right
], dtype=np.float32)

ibo = ctx.buffer(indices)
vbo = ctx.buffer(vertices)
vao = ctx.vertex_array(program, [
        (vbo, '2f', 'in_position'),
    ],
    index_buffer=ibo,
)

running = True

zoom_multiplier = 0.99
zoom_divider = 1.0 / zoom_multiplier
offset_delta = 0.01

zoom = 1.0
offset = [0, 0]

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    keys = pg.key.get_pressed()
    if keys[pg.K_UP]:
        zoom *= zoom_multiplier
    if keys[pg.K_DOWN]:
        zoom *= zoom_divider
    if keys[pg.K_a]: offset[0] -= offset_delta * zoom
    if keys[pg.K_d]: offset[0] += offset_delta * zoom
    if keys[pg.K_s]: offset[1] -= offset_delta * zoom
    if keys[pg.K_w]: offset[1] += offset_delta * zoom



    ctx.clear(0, 0, 0, 1)

    vao.render(mgl.TRIANGLES)
    program['zoom'].value = zoom
    program['offset'].value = offset

    pg.display.flip()

    clock.tick(FPS)

pg.quit()