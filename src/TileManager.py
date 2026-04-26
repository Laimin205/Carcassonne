import json
import pygame as pg
from random import shuffle

from src.Tile import Tile
from settings import TILES_PATH

class TileManager:
    def __init__(self):
        self._tiles_image = pg.image.load(TILES_PATH)
        self._tiles = []
        self._idx = 1
        self._prev_mouse_pos = (0, 0)

        self.create_tiles()

    def create_tiles(self):
        with open('tile_data.json', 'r', encoding='utf-8') as f:
            tiles_data = json.load(f)

        for data in tiles_data:
            for _ in range(data["count"]):
                self._tiles.append(Tile(data, self._tiles_image))

        shuffle(self._tiles)
        initial_one = Tile({'asset_x': 3, 'asset_y': 2, 'sides': ['city', 'road', 'field', 'road']},
                           self._tiles_image)
        initial_one.set_pos(0, 0)
        self._tiles.insert(0, initial_one)

    def draw(self, window):
        for tile in self._tiles:
            tile.draw(window)

    def draw_current_tile(self, window):
        screen, sc, x, y = window.get_for_draw()
        pg.draw.rect(screen, (255, 0, 0), (0, 0, 140, 140))
        self._tiles[self._idx].draw_pos(window, 5, 5, 0.5)

    def handle_event(self, event, window):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._prev_mouse_pos = event.pos
            elif event.button == 3:
                self._tiles[self._idx].rotate()
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and self._prev_mouse_pos == event.pos:
                x, y = event.pos
                self._tiles[self._idx].place(window, x, y)
                self._idx += 1
