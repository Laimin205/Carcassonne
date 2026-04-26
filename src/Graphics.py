import sys
import pygame as pg

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FLAGS, SCALE_DIFF, INIT_GLOB_X, INIT_GLOB_Y, TILE_SIZE

class Graphics:
    def __init__(self):
        self._center_x = INIT_GLOB_X
        self._center_y = INIT_GLOB_Y
        self._scale = 1
        self._prev_mouse_pos = (0, 0)
        self._cur_shift = (0, 0)
        self._is_shifting = False
        self._screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), SCREEN_FLAGS)
        self._color = pg.Color(80, 50, 20)

    def get_for_draw(self):
        dx, dy = self._cur_shift
        return self._screen, self._scale, self._center_x + dx, self._center_y + dy

    def get_screen(self):
        return self._screen

    def get_grid_pos(self, rel_pos):
        rel_x, rel_y = rel_pos
        dx, dy = self._cur_shift
        scaled_size = int(TILE_SIZE * self._scale)
        return ((rel_x - self._center_x - dx) // scaled_size,
                (rel_y - self._center_y - dy) // scaled_size)

    def change_scale(self, idx):
        self._scale += idx * SCALE_DIFF
        if self._scale <= SCALE_DIFF:
            self._scale += SCALE_DIFF

    def update_center(self):
        dx, dy = self._cur_shift
        self._center_x += dx
        self._center_y += dy
        self._cur_shift = (0, 0)

    def handle_event(self, event):
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
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
        self._screen.fill(self._color)
