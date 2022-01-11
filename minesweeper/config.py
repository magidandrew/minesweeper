import pygame as pg
from pathlib import Path

face_icon = pg.image.load(Path("assets/face.png"))
dead_icon = pg.image.load(Path("assets/dead.png"))
win_icon = pg.image.load(Path("assets/win.png"))
bomb_icon = pg.image.load(Path("assets/bomb.png"))
detonated_icon = pg.image.load(Path("assets/detonated.png"))
btn_icon = pg.image.load(Path("assets/button.png"))
flag_icon = pg.image.load(Path("assets/flag.png"))
app_icon = pg.image.load(Path("assets/icon.png"))
depressed_icon = pg.image.load(Path("assets/pressed.png"))

pathlist = Path("assets/numbers").rglob('*.png')
ssd_numbers = [pg.image.load(x) for x in sorted(pathlist)]

DEFAULT_SCREENX = 377
DEFAULT_SCREENY = 497

RESOLUTIONS = {(9, 9): (377, 497), (16, 16): (452, 650), (16, 30): (842, 650)}
FONT_SIZES = {(9, 9): 30, (16, 16): 23, (16, 30): 23}

LINE_WIDTH = 4
THIN_LINE_WIDTH = LINE_WIDTH // 2

# INDICES
MINE_INDEX = 0
HINT_INDEX = 1
X = 0
Y = 1

ROWS = 9
COLS = 9
DIM = (ROWS, COLS)
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
