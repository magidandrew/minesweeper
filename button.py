import pygame as pg


class Button:
    def __init__(self, rect=None):
        self.revealed: bool = False
        self.flagged: bool = False
        self.rect: pg.Rect = rect
