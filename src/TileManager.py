import json
import pygame as pg
from random import shuffle

from src.Tile import Tile
from settings import TILES_PATH


class TileManager:
    def __init__(self):
        self._tiles_image = pg.image.load(TILES_PATH)
        self._tiles = []
        self._idx = 0
        self._prev_mouse_pos = (0, 0)
        self._grid = {}

        self.create_tiles()

    def create_tiles(self):
        with open('tile_data.json', 'r', encoding='utf-8') as f:
            tiles_data = json.load(f)

        for data in tiles_data:
            for _ in range(data["count"]):
                self._tiles.append(Tile(data, self._tiles_image))

        shuffle(self._tiles)
        initial_one = Tile({'asset_x': 3, 'asset_y': 2,
                            'sides': ['city', 'road', 'field', 'road']},
                           self._tiles_image)
        initial_one.set_pos((0, 0))
        self._grid[(0, 0)] = initial_one
        self._idx += 1
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
                grid_pos = window.get_grid_pos(event.pos)
                if self.is_placible_here(self._tiles[self._idx], grid_pos):
                    self._tiles[self._idx].set_pos(grid_pos)
                    self._grid[grid_pos] = self._tiles[self._idx]
                    self._idx += 1

    def is_placible_here(self, cur_tile, grid_pos):
        x, y = grid_pos
        if grid_pos in self._grid:
            return False

        count = 0
        if (x - 1, y) in self._grid:
            count += 1
            if cur_tile.left() != self._grid[(x - 1, y)].right():
                return False

        if (x + 1, y) in self._grid:
            count += 1
            if cur_tile.right() != self._grid[(x + 1, y)].left():
                return False

        if (x, y - 1) in self._grid:
            count += 1
            if cur_tile.up() != self._grid[(x, y - 1)].down():
                return False

        if (x, y + 1) in self._grid:
            count += 1
            if cur_tile.down() != self._grid[(x, y + 1)].up():
                return False

        return count != 0