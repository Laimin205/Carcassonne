"""
TileManager.py

Модуль управления тайлами в игре

Содержит класс TileManager, который отвечает за:
    создание, хранение и управление тайлами
    обработку пользовательского ввода
    проверку правил размещения
"""
import json
import pygame as pg
from random import shuffle

from src.Tile import Tile
from settings import TILES_PATH


class TileManager:
    """
    Менеджер тайлов, отвечающий за игровую механику размещения тайлов

    Attributes:
        _tiles_image (pg.Surface): спрайт-лист всех тайлов
        _tiles (list[Tile]): список всех тайлов в игре, а также "игровой мешок"
        _idx (int): индекс текущего активного тайла в мешке
        _prev_mouse_pos (tuple[int, int]): позиция мыши при нажатии
        _grid (dict[tuple[int, int], Tile]): размещённые тайлы на поле
    """
    def __init__(self):
        """
        Инициализирует менеджер тайлов
        """
        self._tiles_image = pg.image.load(TILES_PATH)
        self._tiles = []
        self._idx = 0
        self._prev_mouse_pos = (0, 0)
        self._grid = {}

        self.create_tiles()

    def create_tiles(self):
        """
        Создаёт все тайлы из файла tile_data.json, и перемешивает их для игры
        Размещает начальный тайл
        """
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
        """
        Отрисовывает все тайлы на экране

        Args:
            window (Graphics): объект окна (интерфейс, предоставляющий глобальные данные)
        """
        for tile in self._tiles:
            tile.draw(window)

    def draw_current_tile(self, window):
        """
        Отрисовывает текущий активный тайл в левом верхнем углу экрана

        Args:
            window (Graphics): объект окна (интерфейс, предоставляющий глобальные данные)
        """
        screen, sc, x, y = window.get_for_draw()
        pg.draw.rect(screen, (255, 0, 0), (0, 0, 140, 140))
        self._tiles[self._idx].draw_pos(window, 5, 5, 0.5)

    def handle_event(self, event, window):
        """
        Обрабатывает события мыши

        Поддерживает:
        - лкм: выбор и размещение тайла
        - лкм: поворот тайла

        Args:
            event (pg.event): событие
            window (Graphics): объект окна (интерфейс, предоставляющий глобальные данные)
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._prev_mouse_pos = event.pos
            elif event.button == 3:
                self._tiles[self._idx].rotate()
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and self._prev_mouse_pos == event.pos:
                grid_pos = window.get_grid_pos(event.pos)
                if self.is_placeable_here(self._tiles[self._idx], grid_pos):
                    self._tiles[self._idx].set_pos(grid_pos)
                    self._grid[grid_pos] = self._tiles[self._idx]
                    self._idx += 1

    def is_placeable_here(self, cur_tile, grid_pos):
        """
        Проверяет возможность размещения тайла в указанной позиции

        Условия:
        - клетка не занята
        - хотя бы одна соседняя клетка существует
        - стороны тайлов совпадают по правилам

        Args:
            cur_tile (Tile): текущий тайл
            grid_pos (tuple[int, int]): координаты на сетке

        Returns:
            bool: True, если тайл можно разместить
        """
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