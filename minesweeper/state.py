from timeit import default_timer as timer
import pygame as pg
import config as cf
from pathlib import Path


class State:
    def __init__(self):
        self.flag_num: int = 0
        self.mine_num: int = cf.DEFAULT_MINE_NUM
        self.won: bool = False
        self.dead: bool = False
        self.rows = cf.ROWS
        self.cols = cf.COLS
        self.running: bool = False
        self.start_time = 0
        self.end_time = 0
        self.face_rect = None

    def update_score_area(self, score_surface: pg.Surface):
        border_offset: int = int(score_surface.get_height() * .25)
        face_size = score_surface.get_height() - border_offset

        def blit_face(icon: pg.image):
            self.face_rect = score_surface.blit(pg.transform.scale(icon, (face_size, face_size)),
                                                (score_surface.get_width() // 2 - face_size // 2, border_offset // 2))

        if not self.won:
            blit_face(cf.face_icon)
        elif self.won:
            blit_face(cf.win_icon)
        if self.dead:
            blit_face(cf.dead_icon)

        digit_height: int = face_size
        digit_width: int = face_size - face_size // 2
        # flag counter
        flag_count: int = self.mine_num - self.flag_num
        digits: list[int] = list(map(int, str(flag_count)))
        while len(digits) < 3:
            digits.insert(0, 0)
        x_pos = border_offset // 2
        for digit in digits:
            score_surface.blit(pg.transform.scale(cf.ssd_numbers[digit],
                                                  (digit_width, digit_height)), (x_pos, border_offset // 2))
            x_pos += digit_width

        # timer
        time_digits: list[int] = list(map(int, str(self.get_time())))
        while len(time_digits) < 3:
            time_digits.insert(0, 0)
        x_pos = score_surface.get_width() - border_offset // 2 - 3 * digit_width
        for digit in time_digits:
            score_surface.blit(pg.transform.scale(cf.ssd_numbers[digit],
                                                  (digit_width, digit_height)), (x_pos, border_offset // 2))
            x_pos += digit_width

    def reset_state(self):
        self.__init__()

    def start_game(self):
        if self.running or self.won or self.dead:
            return
        self.running = True
        self.start_time = timer()

    def get_time(self) -> int:
        if self.running:
            return int(timer() - self.start_time)
        elif self.dead or self.won:
            return int(self.end_time - self.start_time)
        else:
            return 0

    def die(self):
        self.dead = True
        self.running = False
        self.end_time = timer()

    def win(self):
        if not self.won:
            self.running = False
            self.won = True
            self.end_time = timer()

    def terminated_state(self):
        return self.won or self.dead
