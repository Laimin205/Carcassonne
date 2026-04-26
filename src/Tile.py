"""
Tile.py

Модуль для работы с тайлами игрового поля

Содержит класс Tile, который отвечает за:
    извлечение изображения тайла из спрайт-листа
    хранение состояния тайла (позиция, поворот, стороны, статус)
    отображение тайла на экране по заданным параметрам
    управление положением и поворотом тайла
    предоставление информации о сторонах тайла
"""
import pygame as pg

from settings import TILE_SIZE


class Tile:
    """
    Класс, представляющий тайл игрового поля

    Attributes:
        _x_pos (int): координата по Ox в сетке
        _y_pos (int): координата по Oy в сетке
        _rotation (int): угол поворота по часовой стрелке (в градусах)
        _sides (list[str]): типы сторон в порядке [верх, право, низ, лево]
        _status (str): текущее состояние тайла
            - "bag": тайл находится в мешке
            - "hold": тайл примеряется на поле - TODO
            - "placed": тайл размещен на поле
    """
    def __init__(self, data, tiles_image, x_pos = 0, y_pos = 0):
        """
        Инициализирует новый тайл

        Args:
            data (dict): словарь с данными из tile_data.json, содержащий:
                - asset_x (int): позиция тайла по Ox в спрайт-листе
                - asset_y (int): позиция тайла по Oy в спрайт-листе
                - sides (list[str]): типы сторон тайла
            tiles_image (pg.Surface): изображение со всеми тайлами
            x_pos (int): координаты тайла в сетке по Ox
            y_pos (int): координаты тайла в сетке по Oy
        """
        self._sprite = tiles_image.subsurface(
            (TILE_SIZE * data["asset_x"], TILE_SIZE * data["asset_y"],
             TILE_SIZE, TILE_SIZE)).copy()
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._rotation = 0
        self._sides = list(data["sides"])
        self._status = "bag" # "bag", "hold", "placed"

    def draw(self, window):
        """
        Отрисовывает тайл в окне на основе текущего состояния

        Args:
            window (Graphics): класс окна, предоставляющий необходимые для отображения данные (экран, масштаб, смещение)
        """
        if self._status == "bag":
            return

        screen, scale, x, y = window.get_for_draw()
        scaled_size = int(TILE_SIZE * scale)
        scaled_sprite = pg.transform.rotozoom(self._sprite, self._rotation,
                                              scale)
        screen.blit(scaled_sprite, (self._x_pos * scaled_size + x,
                                    self._y_pos * scaled_size + y))

    def draw_pos(self, window, x = 0, y = 0, scale = 1):
        """
        Отображает тайл в окне по заданным координатам и масштабу

        Args:
            window (Graphics): объект окна (интерфейс, предоставляющий глобальные данные)
            x (int): координата левого верхнего угла тайла по Ox в окне
            y (int): координата левого верхнего угла тайла по Oy в окне
            scale (float): масштаб
        """
        screen = window.get_screen()
        scaled_sprite = pg.transform.rotozoom(self._sprite, self._rotation,
                                              scale)
        screen.blit(scaled_sprite, (x, y))

    def set_pos(self, pos):
        """
        Устанавливает позицию тайла в игровой сетке и переводит его в состояние "placed"

        Args:
            pos (tuple[int, int]): координаты клетки в игровой сетке
        """
        x, y = pos
        self._x_pos = x
        self._y_pos = y
        self._status = "placed"

    def rotate(self):
        """
        Поворачивает тайл на 90 градусов по часовой стрелке и обновляет порядок сторон тайла
        """
        self._rotation = (self._rotation + 270) % 360
        self._sides = self._sides[-1:] + self._sides[:-1]

    def up(self):
        """
        Возвращает тип верхней стороны тайла

        Returns:
            str: тип верхней стороны тайла
        """
        return self._sides[0]

    def right(self):
        """
        Возвращает тип правой стороны тайла

        Returns:
            str: тип правой стороны тайла
        """
        return self._sides[1]

    def down(self):
        """
        Возвращает тип нижней стороны тайла

        Returns:
            str: тип нижней стороны тайла
        """
        return self._sides[2]

    def left(self):
        """
        Возвращает тип левой стороны тайла

        Returns:
            str: тип левой стороны тайла
        """
        return self._sides[3]
