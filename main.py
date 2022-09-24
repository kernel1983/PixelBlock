
import time

import pyglet

window = pyglet.window.Window()

label = pyglet.text.Label('Pixel Block',
                          font_name='Monaco Regular',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

# pixels = [
#     255, 0, 0,      0, 255, 0,      0, 0, 255,     # RGB values range from
#     255, 0, 0,      0, 255, 0,      0, 0, 255,     # 0 to 255 for each color
#     255, 0, 0,      0, 255, 0,      0, 0, 255,     # component.
# ]
pixels0 = [0, 0, 0, 255] * 64
pixels1 = [255, 0, 0, 255] * 64
pixels2 = [0, 255, 0, 255] * 64
pixels3 = [0, 0, 255, 255] * 64
pixels4 = [255, 255, 0, 255] * 64
pixels5 = [0, 255, 255, 255] * 64
pixels6 = [255, 0, 255, 255] * 64
pixels7 = [255, 255, 255, 255] * 64
blocks = [pixels1, pixels2, pixels3, pixels4, pixels5, pixels6, pixels7, pixels1, pixels1, pixels0]
current_block = 0

cursor_x = window.width//2 - 8*10
cursor_y = window.height//2 + 8*1
current_x = cursor_x
current_y = cursor_y

key_up = False
key_down = False
key_left = False
key_right = False

map = {}
draw = False
pressed = None

@window.event
def on_draw():
    global map
    window.clear()
    label.draw()

    for x, y in map:
        block_index = map[(x, y)]
        pixels = blocks[block_index]
        raw_data = (pyglet.gl.GLubyte * len(pixels))(*pixels)
        image_data = pyglet.image.ImageData(8, 8, 'RGBA', raw_data)
        image_data.blit(x, y)

    if time.time() % 1.0 > 0.5:
        raw_data = (pyglet.gl.GLubyte * len(pixels1))(*pixels1)
        image_data = pyglet.image.ImageData(8, 8, 'RGBA', raw_data)
        image_data.blit(cursor_x, cursor_y)

@window.event
def on_key_press(symbol, modifiers):
    global key_up
    global key_down
    global key_left
    global key_right

    global pressed
    global current_block

    pressed = time.time()
    print(pressed, symbol)
    if symbol == pyglet.window.key.UP:
        # print(pressed, symbol)
        key_up = True
    elif symbol == pyglet.window.key.DOWN:
        # print(pressed, symbol)
        key_down = True
    elif symbol == pyglet.window.key.LEFT:
        # print(pressed, symbol)
        key_left = True
    elif symbol == pyglet.window.key.RIGHT:
        # print(pressed, symbol)
        key_right = True
    elif symbol == pyglet.window.key.W:
        key_up = True
    elif symbol == pyglet.window.key.S:
        key_down = True
    elif symbol == pyglet.window.key.A:
        key_left = True
    elif symbol == pyglet.window.key.D:
        key_right = True


@window.event
def on_key_release(symbol, modifiers):
    global cursor_x
    global cursor_y
    global current_x
    global current_y

    global map
    global draw
    global current_block
    global pressed

    pressed = None
    if symbol == pyglet.window.key.UP:
        cursor_y = current_y + 8
    elif symbol == pyglet.window.key.DOWN:
        cursor_y = current_y - 8
    elif symbol == pyglet.window.key.LEFT:
        cursor_x = current_x - 8
    elif symbol == pyglet.window.key.RIGHT:
        cursor_x = current_x + 8
    elif symbol == pyglet.window.key.W:
        cursor_y = current_y + 8
    elif symbol == pyglet.window.key.S:
        cursor_y = current_y - 8
    elif symbol == pyglet.window.key.A:
        cursor_x = current_x - 8
    elif symbol == pyglet.window.key.D:
        cursor_x = current_x + 8

    if symbol >= pyglet.window.key._0 and symbol <= pyglet.window.key._9:
        current_block = symbol - pyglet.window.key._1
    elif symbol == pyglet.window.key.SPACE:
        draw = not draw
    elif symbol == pyglet.window.key.ENTER:
        pass
    elif symbol == pyglet.window.key.ESCAPE:
        pass
    elif symbol == pyglet.window.key.DELETE:
        if (current_x, current_y) in map:
            del map[(current_x, current_y)]


def update(dt):
    global cursor_x
    global cursor_y
    global current_x
    global current_y

    global key_up
    global key_down
    global key_left
    global key_right

    global pressed
    global draw


    if pressed:
        if (time.time() - pressed > 0.1):
            # print(key_up, key_down, key_left, key_right)
            if key_up == True:
                cursor_y = current_y + 8
            elif key_down == True:
                cursor_y = current_y - 8
            elif key_left == True:
                cursor_x = current_x - 8
            elif key_right == True:
                cursor_x = current_x + 8
        # else:
        #     print('ok')

    else:
        # print('ignore')
        key_up = False
        key_down = False
        key_left = False
        key_right = False

    if draw and (current_x, current_y) != (cursor_x, cursor_y):
        map[(current_x, current_y)] = current_block

    current_x = cursor_x
    current_y = cursor_y

pyglet.clock.schedule_interval(update, 0.10)

pyglet.app.run()
