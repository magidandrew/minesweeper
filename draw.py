import pygame as pg
import config_globals as gb


def draw_guides(sf: pg.Surface, rows: int, cols: int):
    x_length = sf.get_size()[0]
    y_length = sf.get_size()[1]
    x_delta = int(x_length / cols)
    y_delta = int(y_length / rows)

    x_pos = x_delta
    y_pos = y_delta
    for _ in range(rows - 1):
        pg.draw.line(sf, gb.DARK_GREY, (0, y_pos), (x_length, y_pos))
        pg.draw.line(sf, gb.DARK_GREY, (x_pos, 0), (x_pos, y_length))
        x_pos += x_delta
        y_pos += y_delta