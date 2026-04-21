import pygame as pg

from src.Graphics import Graphics
from src.Tile import Tile


tile1 = Tile(5, 2, 0, 0)
tile2 = Tile(2, 1, 0, -1)
tile3 = Tile(10, 1, 1, 0)
window = Graphics()

while True:
    # 1 - обработка событий
    for event in pg.event.get():
        window.handle_event(event)

    # 2 - обновление логики и параметров

    # 3 - Отрисовка экрана и объектов
    window.draw()
    tile1.draw(window)
    tile2.draw(window)
    tile3.draw(window)
    pg.display.update()
