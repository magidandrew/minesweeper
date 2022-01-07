from timeit import default_timer as timer
import pygame as pg
import config as cf
from pathlib import Path

class State:
    def __init__(self):
        self.flag_num: int = 0
        self.mine_num: int = 0
        self.won: bool = False
        self.dead: bool = False
        self.rows = cf.ROWS
        self.cols = cf.COLS

    def update_score_area(self, score_surface: pg.Surface):
        border_offset: int = int(score_surface.get_height() * .25)
        face_size = score_surface.get_height() - border_offset

        def blit_face(icon: pg.image):
            score_surface.blit(pg.transform.scale(icon, (face_size, face_size)),
                               (score_surface.get_width()//2 - face_size//2, border_offset//2))

        if not self.won:
            blit_face(cf.face_icon)
        elif self.won:
            blit_face(cf.win_icon)
        if self.dead:
            blit_face(cf.dead_icon)

    def reset_state(self):
        self.__init__()