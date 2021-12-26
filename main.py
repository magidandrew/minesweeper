import pygame as pg
import config_globals as gb
from random import random
from pathlib import Path
import pygame_menu as pgm
import sys
from button import Button
import draw as drw

bomb_icon = pg.image.load(Path("assets/bomb.png"))
btn_icon = pg.image.load(Path("assets/button.png"))
flag_icon = pg.image.load(Path("assets/flag.png"))
face_icon = pg.image.load(Path("assets/face.png"))
cool_icon = pg.image.load(Path("assets/cool.png"))
dead_icon = pg.image.load(Path("assets/dead.png"))
app_icon = pg.image.load(Path("assets/icon.png"))

pg.font.init()
font = pg.font.SysFont("Courier", gb.FONT_SIZE, bold=True)
font_width, font_height = font.size("1")

pg.init()
pg.display.set_caption("Minesweeper")
pg.display.set_icon(app_icon)

screen = pg.display.set_mode((gb.SCREENX, gb.SCREENY), pg.RESIZABLE)


def print_mat(mat: list[list[int]]):
    for i in mat:
        print(i)


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


def create_field(x: int, y: int, mine_num: int = 10, mine_prob: float = .2) -> tuple[
    list[list[int]], list[list[int]]]:
    mines = [[0] * y for _ in range(x)]
    hints = [[0] * y for _ in range(x)]
    count = 0

    # pass in bomb location and try to
    def inc_hint(bomb_x: int, bomb_y: int):

        def try_add(hint_x: int, hint_y: int):
            try:
                # prevent negative indexing
                if hint_x < 0 or hint_y < 0:
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

    while count < mine_num:
        for row in range(x):
            for col in range(y):
                if count == mine_num:
                    break
                if random() <= mine_prob and mines[row][col] == 0:
                    # mine added
                    mines[row][col] = 1
                    inc_hint(row, col)
                    count += 1

    for row in range(x):
        for col in range(y):
            if mines[row][col] == 1:
                hints[row][col] = -1

    return mines, hints


def blit_hints_to_surface(fs: pg.Surface, font: pg.font.Font, hint_mat: list[list[int]]):
    rows = len(hint_mat)
    cols = len(hint_mat[0])

    x_delta = int(fs.get_size()[0] / cols)
    y_delta = int(fs.get_size()[1] / rows)
    y_pos = int((y_delta - font_height) / 2)
    # y_pos = 0

    for x in range(rows):
        x_pos = int((x_delta - font_width) / 2)
        for y in range(cols):
            if 0 <= hint_mat[x][y] <= 8:
                fs.blit(font.render(str(hint_mat[x][y]), False, gb.NUMBER2COLOR[str(hint_mat[x][y])]),
                        (x_pos, y_pos, x_delta, y_delta))
            elif hint_mat[x][y] < 0:
                fs.blit(pg.transform.scale(bomb_icon, (font_width, font_height)),
                        (x_pos, y_pos, x_delta, y_delta))
            x_pos += x_delta
        y_pos += y_delta


def update_blit_buttons_to_surface(fs: pg.Surface, rows: int, cols: int, buttons):
    x_delta = int(fs.get_size()[0] / cols)
    y_delta = int(fs.get_size()[1] / rows)
    y_pos = 0

    for x in range(rows):
        x_pos = 0
        for y in range(cols):
            idx = x * cols + y
            if buttons[idx].revealed:
                pass
            elif buttons[idx].flagged:
                fs.blit(pg.transform.scale(flag_icon, (x_delta, y_delta)), (x_pos, y_pos, x_delta, y_delta))
            else:
                fs.blit(pg.transform.scale(btn_icon, (x_delta, y_delta)), (x_pos, y_pos, x_delta, y_delta))
            x_pos += x_delta
        y_pos += y_delta


def create_blit_buttons_to_surface(fs: pg.Surface, rows: int, cols: int):
    x_delta = int(fs.get_size()[0] / cols)
    y_delta = int(fs.get_size()[1] / rows)
    y_pos = 0

    buttons = []
    # pressed_indices = [i[0] for i in pressed]
    for x in range(rows):
        x_pos = 0
        for y in range(cols):
            # extract index
            btn = fs.blit(pg.transform.scale(btn_icon, (x_delta, y_delta)), (x_pos, y_pos, x_delta, y_delta))
            buttons.append(Button(rect=btn))
            # FIXME: THIS IS UNGODLY. NEED SOME STATE CLASSES TO CLEAN THIS UP.
            # elif btn_index in pressed_indices and pressed[[i for i, (v,*_) in enumerate(pressed) if v == btn_index][0]][1] == gb.FLAG:
            #     btn = fs.blit(pg.transform.scale(flag_icon, (x_delta, y_delta)), (x_pos, y_pos, x_delta, y_delta))
            #     buttons.append(btn)
            x_pos += x_delta
        y_pos += y_delta
    return buttons


def main():
    x_offset = int(gb.SCREENX * 0.05)
    y_offset_top = int(gb.SCREENY * 0.2)
    y_offset_bottom = int(gb.SCREENY * 0.03)
    y_offset_score = int(1.5 * y_offset_bottom)

    pressed = []
    buttons = []

    # clear screen
    screen.fill((0, 0, 0, 0))

    # create surface the same size as playing area
    # SRCALPHA for background transparency
    field_surface = pg.Surface((gb.SCREENX - 2 * x_offset - 2 * gb.LINE_WIDTH,
                                gb.SCREENY - y_offset_top - y_offset_bottom - 2 * gb.LINE_WIDTH), pg.SRCALPHA)
    field_surface.fill(gb.GREY)
    buttons_surface = pg.Surface((gb.SCREENX - 2 * x_offset - 2 * gb.LINE_WIDTH,
                                  gb.SCREENY - y_offset_top - y_offset_bottom - 2 * gb.LINE_WIDTH), pg.SRCALPHA)

    field = create_field(8, 8)

    blit_hints_to_surface(field_surface, font, field[gb.HINT_INDEX])
    buttons = create_blit_buttons_to_surface(buttons_surface, 8, 8)

    def redraw_screen():
        nonlocal buttons
        # screen.fill(gb.GREY)
        # draw outside border
        pg.draw.rect(screen, gb.WHITE, (0, 0, gb.SCREENX, gb.SCREENY), gb.LINE_WIDTH, 1)
        # draw playing area
        pg.draw.rect(screen, gb.DARK_GREY, (x_offset, y_offset_top, gb.SCREENX - 2 * x_offset,
                                            gb.SCREENY - y_offset_top - y_offset_bottom), gb.LINE_WIDTH, 1)

        # draw score area
        pg.draw.rect(screen, gb.DARK_GREY, (x_offset, y_offset_bottom, gb.SCREENX - 2 * x_offset,
                                            y_offset_top - y_offset_score), gb.LINE_WIDTH, 1)

        drw.draw_guides(field_surface, 8, 8)

        # reset buttons_surface
        buttons_surface.fill((0, 0, 0, 0))
        update_blit_buttons_to_surface(buttons_surface, 8, 8, buttons)

        screen.blit(field_surface, (x_offset + gb.LINE_WIDTH, y_offset_top + gb.LINE_WIDTH))
        screen.blit(buttons_surface, (x_offset + gb.LINE_WIDTH, y_offset_top + gb.LINE_WIDTH))
        pg.display.update()

    redraw_screen()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # TODO: fix mouse offset without magic numbers
                mouse_pos = (mouse_pos[0] - 23, mouse_pos[1] - 101)
                for btn in buttons:
                    if btn is not None:
                        if btn.rect.collidepoint(mouse_pos):
                            if event.button == pg.BUTTON_LEFT:
                                if not btn.flagged:
                                    btn.revealed = True
                            elif event.button == pg.BUTTON_RIGHT:
                                btn.flagged = not btn.flagged
                            redraw_screen()


def init_and_menu():
    menu = pgm.Menu("MINESW33PER", gb.SCREENX, gb.SCREENY, theme=pgm.themes.THEME_DARK)
    menu.add.selector("Difficulty: ", [("Rookie", 1), ("Apprentice", 2), ("Bomb Tech", 3)])
    menu.add.button("Play", main)
    menu.add.button("Quit", pgm.events.EXIT)
    menu.add.label("\nESC to main menu")
    menu.mainloop(screen)


if __name__ == "__main__":
    # init_and_menu()
    main()
