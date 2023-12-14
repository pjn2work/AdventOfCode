from typing import List


Table = List[List]


def transpose(t: Table) -> Table:
    return [list(column) for column in zip(*t)]


def flip_horizontal(t: Table) -> Table:
    return [list(row)[::-1] for row in t]


def flip_vertical(t: Table) -> Table:
    return t[::-1]


def rotate_right(t: Table) -> Table:
    return [list(reversed(column)) for column in zip(*t)]


def rotate_left(t: Table) -> Table:
    return transpose(flip_horizontal(t))
