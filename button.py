import pygame as pg


class Button:
    def __init__(self, x: int, y: int, rect=None):
        self.revealed: bool = False
        self.flagged: bool = False
        self.x = x
        self.y = y
        self.rect: pg.Rect = rect


def reveal_empty_contiguous_boxes(hint_mat: list[list[int]], x: int, y: int):
    if not hint_mat[x][y] == 0:
        return []

    def iszero_at(x: int, y: int) -> bool:
        if x < 0 or y < 0:
            return False
        try:
            return True if hint_mat[x][y] == 0 else False
        except IndexError:
            return False

    def isvalid_at(x: int, y: int) -> bool:
        if x < 0 or y < 0:
            return False
        try:
            return True if hint_mat[x][y] else False
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
        neighbors = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1),
                     (x + 1, y + 1)]
        lateral_neighbors = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
        for neighbor in neighbors:
            if neighbor in lateral_neighbors and iszero_at(neighbor[0], neighbor[1]):
                update(neighbor[0], neighbor[1])
            try:
                if isvalid_at(neighbor[0], neighbor[1]) and neighbor not in marked:
                    marked.append(neighbor)
            except IndexError:
                pass

    return marked
