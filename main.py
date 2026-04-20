import sys
import pygame as pg
from pygame.locals import *

screen = pg.display.set_mode((1700, 1000))
GLOBAL_SCALE=0.6
GLOBAL_X=0
GLOBAL_Y=0
PRESSED_NOW=False

class Tile:
    _x_pos = 0
    _y_pos = 0
    _size = 64

    def __init__(self, sprite_path="./tiles.png", x = 0, y = 0, size = 256):
        self._sprite = pg.image.load(sprite_path).subsurface((512, 512, size, size)).copy()
        self._x_pos = x
        self._y_pos = y
        self._size = size

    def draw(self):
        scaled_size = int(self._size * GLOBAL_SCALE)
        scaled_sprite = pg.transform.scale(self._sprite, (scaled_size, scaled_size))
        screen.blit(scaled_sprite, (self._x_pos * scaled_size + GLOBAL_X + delta_x,
                                          self._y_pos * scaled_size + GLOBAL_Y + delta_y))


tile1 = Tile(x=1, y=0)
tile2 = Tile(x=0, y=2)

old_mouse_x, old_mouse_y = -1, -1
new_mouse_x, new_mouse_y = 0, 0
delta_x, delta_y = 0, 0

while True:
    # 1 - обработка событий
    for event in pg.event.get():
        screen.set_colorkey()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pg.quit()
            sys.exit()
        elif event.type == MOUSEWHEEL:
            if event.y > 0:
                GLOBAL_SCALE += 0.2
            else:
                GLOBAL_SCALE -= 0.2
                GLOBAL_SCALE = max(0.2, GLOBAL_SCALE)

        buttons = pg.mouse.get_pressed()
        if buttons[0]:
            if (not PRESSED_NOW):
                old_mouse_x, old_mouse_y = pg.mouse.get_pos()
                PRESSED_NOW=True
            else:
                new_mouse_x, new_mouse_y = pg.mouse.get_pos()
                delta_x = new_mouse_x - old_mouse_x
                delta_y = new_mouse_y - old_mouse_y
        if not buttons[0] and PRESSED_NOW:
            GLOBAL_X += delta_x
            GLOBAL_Y += delta_y
            delta_x, delta_y = 0, 0
            PRESSED_NOW=False



    # 2 - обновление логики и параметров

    # 3 - Отрисовка экрана и объектов
    screen.fill(pg.Color(80, 50, 20))
    tile1.draw()
    tile2.draw()
    pg.display.update()
