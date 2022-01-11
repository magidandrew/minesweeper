import pygame as pg

import config as cf
from random import sample
import pygame_menu as pgm
import sys
from button import Button, reveal_empty_contiguous_boxes, reveal_bombs
import draw as drw
from state import State

screen = pg.display.set_mode(cf.RESOLUTIONS[cf.DIM])


def pygame_init():
    pg.init()
    pg.font.init()
    pg.display.set_caption("Minesweeper")
    pg.display.set_icon(cf.app_icon)


def print_mat(mat: list[list[int]]):
    for i in mat:
        print(i)


def create_field(x: int, y: int, click_pos: tuple[int, int] = (0, 0), mine_num: int = cf.DEFAULT_MINE_NUM) -> tuple[
    list[list[int]], list[list[int]]]:
    mines = [[0] * y for _ in range(x)]
    hints = [[0] * y for _ in range(x)]

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

        neighbors = [(bomb_x - 1, bomb_y - 1), (bomb_x, bomb_y - 1), (bomb_x + 1, bomb_y - 1), (bomb_x - 1, bomb_y),
                     (bomb_x + 1, bomb_y), (bomb_x - 1, bomb_y + 1), (bomb_x, bomb_y + 1), (bomb_x + 1, bomb_y + 1)]
        for neighbor in neighbors:
            try_add(neighbor[0], neighbor[1])

    # hack to get from 1D index to 2D index
    def to_2d(idx: int) -> tuple[int, int]:
        return idx // y, idx % y

    # hack to get from 2D index to 1D index
    def to_1d(idx: tuple[int, int]) -> int:
        return idx[0] * y + idx[1]

    sampled = [to_1d(click_pos)]
    while to_1d(click_pos) in sampled:
        sampled = sample([x for x in range(x * y)], mine_num)

    for idx in sampled:
        row, col = to_2d(idx)
        if not mines[row][col]:
            mines[row][col] = 1
            inc_hint(row, col)

    for row in range(x):
        for col in range(y):
            if mines[row][col] == 1:
                hints[row][col] = -1

    return mines, hints


def blit_hints_to_surface(fs: pg.Surface, hint_mat: list[list[int]]):
    rows = len(hint_mat)
    cols = len(hint_mat[0])

    # fonts
    font = pg.font.SysFont("Courier", cf.FONT_SIZES[cf.DIM], bold=True)
    font_width, font_height = font.size("1")  # courier is monospaced --> can take size of any char

    x_delta = fs.get_size()[0] // cols
    y_delta = fs.get_size()[1] // rows
    y_pos = (y_delta - font_height) // 2
    y_mine_pos = 0

    for x in range(rows):
        x_pos = (x_delta - font_width) // 2
        x_mine_pos = 0
        for y in range(cols):
            if 0 < hint_mat[x][y] <= 8:
                fs.blit(font.render(str(hint_mat[x][y]), False, cf.NUMBER2COLOR[str(hint_mat[x][y])]),
                        (x_pos, y_pos, x_delta, y_delta))
            elif hint_mat[x][y] < 0:
                fs.blit(pg.transform.scale(cf.bomb_icon, (x_delta, y_delta)),
                        (x_mine_pos, y_mine_pos, x_delta, y_delta))
            x_pos += x_delta
            x_mine_pos += x_delta
        y_pos += y_delta
        y_mine_pos += y_delta


def update_blit_buttons_to_surface(fs: pg.Surface, rows: int, cols: int, buttons):
    x_delta = fs.get_size()[0] // cols
    y_delta = fs.get_size()[1] // rows
    y_pos = 0

    for x in range(rows):
        x_pos = 0
        for y in range(cols):
            idx = x * cols + y
            if buttons[idx].detonated:
                fs.blit(pg.transform.scale(cf.detonated_icon, (x_delta, y_delta)), (x_pos, y_pos, x_delta, y_delta))
            elif buttons[idx].revealed:
                pass
            elif buttons[idx].flagged:
                fs.blit(pg.transform.scale(cf.flag_icon, (x_delta, y_delta)), (x_pos, y_pos, x_delta, y_delta))
            else:
                fs.blit(pg.transform.scale(cf.btn_icon, (x_delta, y_delta)), (x_pos, y_pos, x_delta, y_delta))
            x_pos += x_delta
        y_pos += y_delta


def create_blit_buttons_to_surface(fs: pg.Surface, rows: int, cols: int):
    x_delta = fs.get_size()[0] // cols
    y_delta = fs.get_size()[1] // rows
    y_pos = 0
    buttons = []

    for x in range(rows):
        x_pos = 0
        for y in range(cols):
            btn = fs.blit(pg.transform.scale(cf.btn_icon, (x_delta, y_delta)), (x_pos, y_pos, x_delta, y_delta))
            buttons.append(Button(x, y, rect=btn))
            x_pos += x_delta
        y_pos += y_delta
    return buttons


def main(*args):
    mainloop = True
    while mainloop:
        screen = pg.display.set_mode(cf.RESOLUTIONS[cf.DIM])
        gs = State()
        x_offset = int(cf.RESOLUTIONS[cf.DIM][cf.X] * 0.05)  # this rounds down to 18
        y_offset_top = int(cf.RESOLUTIONS[cf.DIM][cf.Y] * 0.196)  # this rounds down to 97
        y_offset_bottom = int(cf.RESOLUTIONS[cf.DIM][cf.Y] * 0.03)
        y_offset_score = int(1.5 * y_offset_bottom)

        # clear screen
        screen.fill((0, 0, 0, 0))

        # create surface the same size as playing area
        # SRCALPHA for background transparency
        field_surface = pg.Surface((cf.RESOLUTIONS[cf.DIM][cf.X] - 2 * x_offset - 2 * cf.LINE_WIDTH,
                                    cf.RESOLUTIONS[cf.DIM][cf.Y] - y_offset_top - y_offset_bottom - 2 * cf.LINE_WIDTH),
                                   pg.SRCALPHA)
        field_surface.fill(cf.GREY)
        buttons_surface = pg.Surface((cf.RESOLUTIONS[cf.DIM][cf.X] - 2 * x_offset - 2 * cf.LINE_WIDTH,
                                      cf.RESOLUTIONS[cf.DIM][
                                          cf.Y] - y_offset_top - y_offset_bottom - 2 * cf.LINE_WIDTH),
                                     pg.SRCALPHA)

        field = create_field(cf.ROWS, cf.COLS, mine_num=cf.DEFAULT_MINE_NUM)

        score_surface = pg.Surface((cf.RESOLUTIONS[cf.DIM][cf.X] - 2 * x_offset - 2 * cf.LINE_WIDTH,
                                    y_offset_top - y_offset_score - 2 * cf.LINE_WIDTH), pg.SRCALPHA)

        buttons = create_blit_buttons_to_surface(buttons_surface, cf.ROWS, cf.COLS)

        def redraw_screen():
            # nonlocal buttons
            screen.fill(cf.GREY)
            # draw outside border
            pg.draw.rect(screen, cf.WHITE, (0, 0, cf.RESOLUTIONS[cf.DIM][cf.X], cf.RESOLUTIONS[cf.DIM][cf.Y]),
                         cf.LINE_WIDTH, 1)
            # draw playing area
            pg.draw.rect(screen, cf.DARK_GREY, (x_offset, y_offset_top, cf.RESOLUTIONS[cf.DIM][cf.X] - 2 * x_offset,
                                                cf.RESOLUTIONS[cf.DIM][cf.Y] - y_offset_top - y_offset_bottom),
                         cf.LINE_WIDTH, 1)

            # draw score area
            pg.draw.rect(screen, cf.DARK_GREY, (x_offset, y_offset_bottom, cf.RESOLUTIONS[cf.DIM][cf.X] - 2 * x_offset,
                                                y_offset_top - y_offset_score), cf.LINE_WIDTH, 1)

            # clear field_surface
            field_surface.fill(cf.GREY)
            drw.draw_guides(field_surface, cf.ROWS, cf.COLS)

            # blit hints
            blit_hints_to_surface(field_surface, field[cf.HINT_INDEX])

            # reset buttons_surface
            buttons_surface.fill((0, 0, 0, 0))
            update_blit_buttons_to_surface(buttons_surface, cf.ROWS, cf.COLS, buttons)

            gs.update_score_area(score_surface)

            screen.blit(field_surface, (x_offset + cf.LINE_WIDTH, y_offset_top + cf.LINE_WIDTH))
            screen.blit(buttons_surface, (x_offset + cf.LINE_WIDTH, y_offset_top + cf.LINE_WIDTH))
            screen.blit(score_surface, (x_offset + cf.LINE_WIDTH, y_offset_bottom + cf.LINE_WIDTH))
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
                        mainloop = False
                        # set to default resolution
                        screen = pg.display.set_mode((cf.DEFAULT_SCREENX, cf.DEFAULT_SCREENY))

                if event.type == pg.MOUSEBUTTONDOWN:
                    gs.start_game()

                    # in score surface
                    mouse_pos_score = (
                        event.pos[0] - x_offset - cf.LINE_WIDTH, event.pos[1] - y_offset_bottom - cf.LINE_WIDTH)
                    if score_surface.get_rect().collidepoint(mouse_pos_score[0], mouse_pos_score[1]):
                        if gs.face_rect.collidepoint(mouse_pos_score[0], mouse_pos_score[1]):
                            running = False

                    # in play surface
                    mouse_pos_play = (
                    event.pos[0] - x_offset - cf.LINE_WIDTH, event.pos[1] - y_offset_top - cf.LINE_WIDTH)
                    if buttons_surface.get_rect().collidepoint(mouse_pos_play[0], mouse_pos_play[1]):
                        for btn in buttons:
                            if btn is not None:
                                if btn.rect.collidepoint(mouse_pos_play):
                                    if event.button == pg.BUTTON_LEFT:
                                        if not btn.flagged:
                                            # fist move (haven't opened any buttons)
                                            if not len([x for x in buttons if x.revealed]):
                                                field = create_field(cf.ROWS, cf.COLS, (btn.x, btn.y),
                                                                     cf.DEFAULT_MINE_NUM)
                                            # clicked mine
                                            if field[cf.HINT_INDEX][btn.x][btn.y] == -1 and not gs.terminated_state():
                                                gs.die()
                                                btn.detonated = True
                                                for idx in reveal_bombs(field[cf.HINT_INDEX]):
                                                    buttons[idx[0] * cf.COLS + idx[1]].revealed = True
                                            elif not gs.terminated_state():
                                                btn.revealed = True
                                                # set all non-revealed
                                                for idx in reveal_empty_contiguous_boxes(field[cf.HINT_INDEX], btn.x,
                                                                                         btn.y, buttons):
                                                    buttons[idx[0] * cf.COLS + idx[1]].revealed = True
                                    elif event.button == pg.BUTTON_RIGHT and not gs.terminated_state() and not btn.revealed:
                                        if not btn.flagged and gs.flag_num >= gs.mine_num:
                                            continue
                                        btn.flagged = not btn.flagged
                                        if btn.flagged:  # we just incremented
                                            gs.flag_num += 1
                                        else:  # we just decremented
                                            gs.flag_num -= 1
                    # check win
                    if cf.DIM[cf.X] * cf.DIM[cf.Y] - len([x for x in buttons if x.revealed]) == gs.mine_num:
                        gs.win()
            redraw_screen()
        gs.reset_state()


def change_difficulty(*args):
    cf.ROWS = args[0][0][1][0]
    cf.COLS = args[0][0][1][1]
    cf.DEFAULT_MINE_NUM = args[0][0][1][2]
    cf.DIM = (cf.ROWS, cf.COLS)
    args[2].set_title(f"{args[1][0]}x{args[1][1]} grid : {args[1][2]} mines")


def init_and_menu():
    pygame_init()
    menu = pgm.Menu("MINESW33PER", cf.RESOLUTIONS[cf.DIM][cf.X], cf.RESOLUTIONS[cf.DIM][cf.Y],
                    theme=pgm.themes.THEME_DARK)
    description_lbl = pgm.widgets.widget.label.Label(f"{cf.ROWS}x{cf.COLS} grid : {cf.DEFAULT_MINE_NUM} mines")
    description_lbl.is_selectable = False
    menu.add.selector("Difficulty: ",
                      [("Rookie", (cf.ROWS, cf.COLS, cf.DEFAULT_MINE_NUM), description_lbl),
                       ("Apprentice", (16, 16, 40), description_lbl),
                       ("Bomb Tech", (16, 30, 99), description_lbl)], onchange=change_difficulty)
    menu.add.button("Play", main)
    menu.add.button("Quit", pgm.events.EXIT)
    menu.add.label("")  # blank line for spacing
    menu.add.generic_widget(description_lbl, configure_defaults=True)
    menu.add.label("ESC to main menu")
    menu.mainloop(screen)


if __name__ == "__main__":
    init_and_menu()
