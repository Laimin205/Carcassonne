import pygame as pg

from src.Graphics import Graphics
from src.TileManager import TileManager

pg.init()
TM = TileManager()
window = Graphics()

while True:
    # 1 - обработка событий
    for event in pg.event.get():
        window.handle_event(event)
        TM.handle_event(event, window)

    # 2 - обновление логики и параметров

    # 3 - Отрисовка экрана и объектов
    window.draw()
    TM.draw(window)
    TM.draw_current_tile(window)
    pg.display.update()
