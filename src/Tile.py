import pygame as pg

from settings import TILE_SIZE, TILES_PATH

class Tile:
    def __init__(self, asset_x = 0, asset_y = 0, x_pos = 0, y_pos = 0):
        self._sprite = pg.image.load(TILES_PATH).subsurface((TILE_SIZE * asset_x, TILE_SIZE * asset_y,
                                                              TILE_SIZE, TILE_SIZE)).copy()
        self._x_pos = x_pos
        self._y_pos = y_pos

    def set_pos(self, x, y):
        self._x_pos = x
        self._y_pos = y

    def draw(self, window):
        screen, scale, x, y = window.get_for_draw()
        scaled_size = int(TILE_SIZE * scale)
        scaled_sprite = pg.transform.scale(self._sprite, (scaled_size, scaled_size))
        screen.blit(scaled_sprite, (self._x_pos * scaled_size + x,
                                    self._y_pos * scaled_size + y))
