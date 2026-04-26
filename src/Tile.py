import pygame as pg

from settings import TILE_SIZE


class Tile:
    def __init__(self, data, tiles_image, x_pos = 0, y_pos = 0):
        self._sprite = tiles_image.subsurface(
            (TILE_SIZE * data["asset_x"], TILE_SIZE * data["asset_y"],
             TILE_SIZE, TILE_SIZE)).copy()
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._rotation = 0
        self._sides = data["sides"]
        self._status = "bag" # "bag", "hold", "placed"

    def draw(self, window):
        if self._status == "bag":
            return

        screen, scale, x, y = window.get_for_draw()
        scaled_size = int(TILE_SIZE * scale)
        scaled_sprite = pg.transform.rotozoom(self._sprite, self._rotation,
                                              scale)
        screen.blit(scaled_sprite, (self._x_pos * scaled_size + x,
                                    self._y_pos * scaled_size + y))

    def draw_pos(self, window, x = 0, y = 0, scale = 1):
        screen = window.get_screen()
        scaled_sprite = pg.transform.rotozoom(self._sprite, self._rotation,
                                              scale)
        screen.blit(scaled_sprite, (x, y))

    def set_pos(self, pos):
        x, y = pos
        self._x_pos = x
        self._y_pos = y
        self._status = "placed"

    def rotate(self):
        self._rotation = (self._rotation + 270) % 360
        self._sides = self._sides[-1:] + self._sides[:-1]

    def up(self):
        return self._sides[0]

    def right(self):
        return self._sides[1]

    def down(self):
        return self._sides[2]

    def left(self):
        return self._sides[3]