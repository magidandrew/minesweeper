import pygame as pg


class Button:
    def __init__(self, rect=None):
        self.revealed: bool = False
        self.flagged: bool = False
        self.rect: pg.Rect = rect


def reveal_empty_contiguous_boxes(buttons: list[Button], hint_mat: list[list[int]], x: int, y: int):
    if not hint_mat[x][y] == 0:
        return []

    def iszero_at(x: int, y: int) -> bool:
        if x < 0 or y < 0:
            return False
        try:
            return True if hint_mat[x][y] == 0 else False
        except IndexError:
            return False

    def update(new_x, new_y):
        if (new_x, new_y) not in marked:
            marked.append((new_x, new_y))
            queued.append((new_x, new_y))

    queued = [(x, y)]
    marked = [(x, y)]
    while len(queued) != 0:
        x, y = queued.pop()
        if iszero_at(x - 1, y - 1):
            update(x - 1, y - 1)
        if iszero_at(x, y - 1):
            update(x, y - 1)
        if iszero_at(x + 1, y - 1):
            update(x + 1, y - 1)
        if iszero_at(x - 1, y):
            update(x - 1, y)
        if iszero_at(x + 1, y):
            update(x + 1, y)
        if iszero_at(x - 1, y + 1):
            update(x - 1, y + 1)
        if iszero_at(x, y + 1):
            update(x, y + 1)
        if iszero_at(x + 1, y + 1):
            update(x + 1, y + 1)
    return marked
