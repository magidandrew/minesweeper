import pygame as pg
import config_globals as gb
from random import random
from pathlib import Path


def print_mat(mat: list[list[int]]):
    for i in mat:
        print(i)


def create_field(x: int, y: int, mine_num: int = 20, mine_prob: float = .2) -> tuple[
        list[list[int]], list[list[int]]]:
    mines = [[0] * y for _ in range(x)]
    hints = [[0] * y for _ in range(x)]
    count = 0

    # pass in bomb location and try to
    def inc_hint(bomb_x: int, bomb_y: int):

        def try_add(hint_x: int, hint_y: int):
            try:
                # prevent negative indexing
                if bomb_x < 0 or bomb_y < 0:
                    return
                # check that bomb doesn't exist at that location
                if mines[hint_x][hint_y] == 1:
                    return
                hints[hint_x][hint_y] += 1
            except IndexError:
                pass

        try_add(bomb_x - 1, bomb_y - 1)  # Top Left
        try_add(bomb_x, bomb_y - 1)  # Top Middle
        try_add(bomb_x + 1, bomb_y - 1)  # Top Right
        try_add(bomb_x - 1, bomb_y)  # Left
        try_add(bomb_x + 1, bomb_y)  # Right
        try_add(bomb_x - 1, bomb_y + 1)  # Lower Left
        try_add(bomb_x, bomb_y + 1)  # Lower Middle
        try_add(bomb_x + 1, bomb_y + 1)  # Lower Right

    def gen(count, mines):
        for row in range(x):
            for col in range(y):
                if count == mine_num:
                    break
                if random() <= mine_prob and mines[row][col] == 0:
                    # mine added
                    mines[row][col] = 1
                    inc_hint(row, col)
                    count += 1

    if count < mine_num:
        gen(count, mines)
    return mines, hints


def create_hint_mat(mine_mat: list[list[int]]) -> list[list[int]]:
    def isbomb_at(x: int, y: int) -> int:
        if x < 0 or y < 0:
            return 0
        try:
            return 1 if mine_mat[x][y] != 0 else 0
        except IndexError:
            return 0

    rows = len(mine_mat)
    cols = len(mine_mat[0])
    hints = [[0] * cols for _ in range(rows)]
    for x in range(rows):
        for y in range(cols):
            hints[x][y] += isbomb_at(x - 1, y - 1)  # Top Left
            hints[x][y] += isbomb_at(x, y - 1)  # Top Middle
            hints[x][y] += isbomb_at(x + 1, y - 1)  # Top Right
            hints[x][y] += isbomb_at(x - 1, y)  # Left
            hints[x][y] += isbomb_at(x + 1, y)  # Right
            hints[x][y] += isbomb_at(x - 1, y + 1)  # Lower Left
            hints[x][y] += isbomb_at(x, y + 1)  # Lower Middle
            hints[x][y] += isbomb_at(x + 1, y + 1)  # Lower Right
    return hints


def main():
    pg.init()
    pg.display.set_caption("Minesweeper")
    pg.display.set_icon(pg.image.load(Path("img/bomb.png")))

    screen = pg.display.set_mode((gb.SCREENX, gb.SCREENY))
    screen.fill(gb.GREY)

    # each block 8x8 pixel, 8x8 grid of blocks
    # draw outside border
    pg.draw.rect(screen, gb.WHITE, (0, 0, gb.SCREENX, gb.SCREENY), gb.LINE_WIDTH, 1)

    x_offset = int(gb.SCREENX * 0.05)
    y_offset_top = int(gb.SCREENY * 0.2)
    y_offset_bottom = int(gb.SCREENY * 0.03)
    y_offset_score = int(1.5 * y_offset_bottom)
    # draw playing area
    pg.draw.rect(screen, gb.DARK_GREY, (x_offset, y_offset_top, gb.SCREENX - 2 * x_offset,
                                        gb.SCREENY - y_offset_top - y_offset_bottom), gb.LINE_WIDTH, 1)

    # draw score area
    pg.draw.rect(screen, gb.RED, (x_offset, y_offset_bottom, gb.SCREENX - 2 * x_offset,
                                  y_offset_top - y_offset_score), gb.LINE_WIDTH, 1)

    running = True
    while running:
        pg.display.update()

        # quit event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


if __name__ == "__main__":
    # main()
    mat = create_field(8, 8, mine_num=10)
    print_mat(mat[0])
    print("hints")
    print_mat(mat[1])
    # print_mat(create_hint_mat(mat))
