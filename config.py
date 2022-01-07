import pygame as pg
from pathlib import Path

face_icon = pg.image.load(Path("assets/face.png"))
dead_icon = pg.image.load(Path("assets/dead.png"))
win_icon = pg.image.load(Path("assets/win.png"))

SCREENX = 377
SCREENY = 497

LINE_WIDTH = 4
THIN_LINE_WIDTH = int(LINE_WIDTH / 2)

FONT_SIZE = 30

MINE_INDEX = 0
HINT_INDEX = 1

ROWS = 9
COLS = 9
DEFAULT_MINE_NUM = 10
MINE_PROB = .2

# RGB COLOR TUPLES
GREY = (185, 185, 185)
DARK_GREY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 31, 241)
DARK_BLUE = (0, 10, 122)
GREEN = (55, 122, 33)
RED = (232, 50, 35)
DARK_RED = (181, 48, 35)
MAROON = (115, 20, 12)
TEAL = (55, 126, 126)

# COLOR LOOKUP
NUMBER2COLOR = {'0': WHITE, '1': BLUE, '2': GREEN, '3': RED, '4': DARK_BLUE, '5': MAROON, '6': TEAL, '7': BLACK,
                '8': DARK_GREY}
