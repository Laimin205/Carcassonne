import pygame as pg

from settings import TILE_SIZE

class Tile:
    def __init__(self, data, tiles_image, x_pos = 0, y_pos = 0):
        self._sprite = tiles_image.subsurface(
            (TILE_SIZE * data["asset_x"], TILE_SIZE * data["asset_y"], TILE_SIZE, TILE_SIZE)).copy()
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
        scaled_sprite = pg.transform.rotozoom(self._sprite, self._rotation, scale)
        screen.blit(scaled_sprite, (self._x_pos * scaled_size + x,
                                    self._y_pos * scaled_size + y))

    def draw_pos(self, window, x = 0, y = 0, scale = 1):
        screen, sc, _x, _y = window.get_for_draw()
        scaled_sprite = pg.transform.rotozoom(self._sprite, self._rotation, scale)
        screen.blit(scaled_sprite, (x, y))

    def set_pos(self, x, y):
        self._x_pos = x
        self._y_pos = y
        self._status = "placed"

    def rotate(self, angle = -90):
        self._rotation = (self._rotation + angle + 360) % 360

    def place(self, window, rel_x, rel_y):
        screen, scale, gl_x, gl_y = window.get_for_draw()
        scaled_size = int(TILE_SIZE * scale)
        self.set_pos((rel_x - gl_x) // scaled_size, (rel_y - gl_y) // scaled_size)
