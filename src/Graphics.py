"""
Graphics.py

Модуль управления графическим окном и системой отображения

Содержит класс Graphics, отвечающий за:
   создание окна pygame
   управление масштабом (zoom)
   управление смещением "камеры"
   преобразование экранных координат в координаты игровой сетки
   обработку системных событий (закрытие, ESC, прокрутка, перетаскивание)
   отрисовку фона
"""
import sys
import pygame as pg

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FLAGS, SCALE_DIFF, \
   INIT_GLOB_X, INIT_GLOB_Y, TILE_SIZE


class Graphics:
   """
    Класс, представляющий собой систему "камеры" для управления отображением игрового поля

    Attributes:
        _center_x (int): фиксированное смещение камеры по X
        _center_y (int): фиксированное смещение камеры по Y
        _scale (float): текущий масштаб отображения
        _prev_mouse_pos (tuple[int, int]): позиция мыши при начале перетаскивания
        _cur_shift (tuple[int, int]): текущее временное смещение камеры
        _is_shifting (bool): флаг перетаскивания камеры
        _screen (pg.Surface): главное окно pygame
        _color (pg.Color): цвет фона
    """
   def __init__(self):
       """
       Инициализирует графическую систему, создаёт окно pygame и устанавливает начальные параметры
       """
       self._center_x = INIT_GLOB_X
       self._center_y = INIT_GLOB_Y
       self._scale = 1
       self._prev_mouse_pos = (0, 0)
       self._cur_shift = (0, 0)
       self._is_shifting = False
       self._screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                          SCREEN_FLAGS)
       self._color = pg.Color(80, 50, 20)

   def get_for_draw(self):
       """
       Возвращает параметры для отрисовки объектов

       Returns:
           tuple:
               pg.Surface: экран pygame
               float: текущий масштаб
               int: смещение по X
               int: смещение по Y
       """
       dx, dy = self._cur_shift
       return self._screen, self._scale, self._center_x + dx, self._center_y + dy

   def get_screen(self):
       """
       Возвращает основной экран pygame

       Returns:
           pg.Surface: экран pygame
       """
       return self._screen

   def get_grid_pos(self, rel_pos):
       """
        Преобразует координаты экрана в координаты игровой сетки

        Args:
            rel_pos (tuple[int, int]): координаты мыши на экране

        Returns:
            tuple[int, int]: координаты клетки в игровой сетке
        """
       rel_x, rel_y = rel_pos
       dx, dy = self._cur_shift
       scaled_size = int(TILE_SIZE * self._scale)
       return ((rel_x - self._center_x - dx) // scaled_size,
               (rel_y - self._center_y - dy) // scaled_size)

   def change_scale(self, idx):
       """
       Изменяет масштаб отображения

       Args:
           idx (int): направление изменения масштаба колесиком мыши
       """
       self._scale += idx * SCALE_DIFF
       if self._scale <= SCALE_DIFF:
           self._scale += SCALE_DIFF

   def update_center(self):
       """
       Фиксирует текущее смещение камеры
       """
       dx, dy = self._cur_shift
       self._center_x += dx
       self._center_y += dy
       self._cur_shift = (0, 0)

   def handle_event(self, event):
       """
       Обрабатывает системные события

       Поддерживает:
       - выход из игры (QUIT / ESC)
       - масштабирование (колесико мыши)
       - перемещение камеры (зажатая ЛКМ + drag)

       Args:
           event (pg.event): событие pygame
       """
       if event.type == pg.QUIT or (
               event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
           pg.quit()
           sys.exit()

       elif event.type == pg.MOUSEWHEEL:
           self.change_scale(event.y)

       buttons = pg.mouse.get_pressed()
       if buttons[0] and not self._is_shifting:
           self._prev_mouse_pos = pg.mouse.get_pos()
           self._is_shifting = True

       elif buttons[0] and self._is_shifting:
           new_x, new_y = pg.mouse.get_pos()
           old_x, old_y = self._prev_mouse_pos
           self._cur_shift = (new_x - old_x, new_y - old_y)

       elif not buttons[0] and self._is_shifting:
           self.update_center()
           self._is_shifting=False

   def draw(self):
       """
       Подготавливает экран к новому кадру - заливает экран сплошным цветом
       """
       self._screen.fill(self._color)

