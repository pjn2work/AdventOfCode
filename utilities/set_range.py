from __future__ import annotations
from collections import namedtuple
from typing import List, Tuple, Dict

import re


INTERSECT_NONE = 0
INTERSECT_LEFT = 1
INTERSECT_MIDDLE = 2
INTERSECT_RIGHT = 3
INTERSECT_ALL = 4


Limits = namedtuple("Limits", "y0 x0 y1 x1")


def get_intersect_type(lx1: int, rx1: int, lx2: int, rx2: int) -> int:
    if rx1 + 1 < lx2 or lx1 - 1 > rx2:
        return INTERSECT_NONE
    if lx2 <= lx1 and rx1 <= rx2:
        return INTERSECT_ALL
    if lx1 <= lx2 and rx2 <= rx1:
        return INTERSECT_MIDDLE
    if lx2 <= lx1:
        return INTERSECT_LEFT
    return INTERSECT_RIGHT


class SetRange1D:
    def __init__(self, lx: int = None, rx: int = None):
        self._set_range: List[Tuple[int, int]] = []
        if lx is not None and rx is not None:
            self.add(lx, rx)
        self._current_index = 0

    @staticmethod
    def __assert_other(other):
        if not isinstance(other, SetRange1D):
            raise TypeError(f"other not of type <class SetRange1D> but {type(other)}")

    def __merge_if_overlap(self):
        idx = 0
        while idx < len(self._set_range) - 1:
            (lx1, rx1), (lx2, rx2) = self._set_range[idx], self._set_range[idx + 1]
            if rx1 + 1 >= lx2:
                self._set_range[idx] = (lx1, max(rx1, rx2))
                del self._set_range[idx + 1]
            else:
                idx += 1

    def add(self, lx: int, rx: int) -> SetRange1D:
        sr = self.get_occupied_as_list()
        lx, rx = min(lx, rx), max(lx, rx)
        for i, (lx2, rx2) in enumerate(sr):
            if rx + 1 < lx2 or lx - 1 > rx2:
                continue
            sr[i] = (min(lx2, lx), max(rx2, rx))
            self.__merge_if_overlap()
            return self

        sr.append((lx, rx))
        sr.sort()
        return self

    def add_from_list(self, data: List[Tuple[int, int]]) -> SetRange1D:
        for lx, rx in data:
            self.add(lx, rx)
        return self

    def sub(self, lx: int, rx: int) -> SetRange1D:
        lx, rx = min(lx, rx), max(lx, rx)
        idx, sr = 0, self.get_occupied_as_list()
        while idx < len(sr):
            lx1, rx1 = sr[idx]
            if lx1 > rx:
                break

            it = get_intersect_type(lx1, rx1, lx, rx)
            if it == INTERSECT_NONE:
                idx += 1
            elif it == INTERSECT_ALL:
                del sr[idx]
            elif it == INTERSECT_LEFT:
                sr[idx] = (rx + 1, rx1)
                idx += 1
            elif it == INTERSECT_RIGHT:
                sr[idx] = (lx1, lx - 1)
                idx += 1
            else:  # INTERSECT_MIDDLE
                sr[idx] = (lx1, lx - 1)
                self.add(rx + 1, rx1)
                return self
        return self

    def copy(self) -> SetRange1D:
        res = SetRange1D()
        res._set_range = self._set_range.copy()
        return res

    def clear(self) -> SetRange1D:
        self._set_range.clear()
        return self

    def __iadd__(self, other: SetRange1D) -> SetRange1D:
        if isinstance(other, int):
            self.add(other, other)
        elif isinstance(other, (tuple, list)) and len(other) == 2:
            self.add(other[0], other[1])
        else:
            self.__assert_other(other)
            for lx, rx in other.get_occupied_as_list():
                self.add(lx, rx)
        return self

    def __isub__(self, other: SetRange1D) -> SetRange1D:
        if isinstance(other, int):
            self.sub(other, other)
        elif isinstance(other, (tuple, list)) and len(other) == 2:
            self.sub(other[0], other[1])
        else:
            self.__assert_other(other)
            for lx, rx in other.get_occupied_as_list():
                self.sub(lx, rx)
        return self

    def __add__(self, other: SetRange1D) -> SetRange1D:
        return self.copy().__iadd__(other)

    def __sub__(self, other: SetRange1D) -> SetRange1D:
        return self.copy().__isub__(other)

    def __invert__(self) -> SetRange1D:
        res = SetRange1D()
        res._set_range = self.get_available_as_list()
        return res

    def __lshift__(self, n: int) -> SetRange1D:
        for i in range(len(self._set_range)):
            lx, rx = self._set_range[i]
            self._set_range[i] = (lx - n, rx - n)
        return self

    def __rshift__(self, n: int) -> SetRange1D:
        for i in range(len(self._set_range)):
            lx, rx = self._set_range[i]
            self._set_range[i] = (lx + n, rx + n)
        return self

    def __bool__(self) -> bool:
        return bool(self._set_range)

    def __eq__(self, other) -> bool:
        self.__assert_other(other)
        return self.get_occupied_as_list() == other.get_occupied_as_list()

    def __contains__(self, item) -> bool:
        if isinstance(item, int):
            for lx, rx in self.get_occupied_as_list():
                if lx <= item <= rx:
                    return True
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            lx2, rx2 = item
            for lx, rx in self.get_occupied_as_list():
                if lx <= lx2 <= rx2 <= rx:
                    return True
        elif isinstance(item, SetRange1D):
            sr1 = self.get_occupied_as_list()
            l1, i1 = len(sr1), 0
            if l1 == 0:
                return False

            lx1, rx1 = sr1[i1]
            for lx2, rx2 in item.get_occupied_as_list():
                while rx1 < lx2:
                    i1 += 1
                    if i1 == l1:
                        return False
                    lx1, rx1 = sr1[i1]

                if not lx1 <= lx2 <= rx2 <= rx1:
                    return False
            return True

        return False

    def __iter__(self) -> Tuple[int, int]:
        for o in self.get_occupied_as_list():
            yield o

    def __next__(self) -> Tuple[int, int]:
        o = self.get_occupied_as_list()
        if self._current_index < len(o):
            self._current_index += 1
            return o[self._current_index - 1]
        self._current_index = 0
        raise StopIteration

    def __str__(self) -> str:
        return str(self.get_occupied_as_list())

    def __repr__(self) -> str:
        return str(self.get_occupied_as_list())

    def get_occupied_as_list(self) -> List[Tuple[int, int]]:
        return self._set_range

    def get_available_as_list(self) -> List[Tuple[int, int]]:
        res = []
        if len(self._set_range) > 1:
            for (_, rx1), (lx2, _) in zip(self._set_range, self._set_range[1:]):
                res.append((rx1 + 1, lx2 - 1))
        return res

    def get_available(self) -> SetRange1D:
        return SetRange1D().add_from_list(self.get_available_as_list())

    def get_inner_join(self, other: SetRange1D) -> SetRange1D:
        self.__assert_other(other)
        res = SetRange1D()
        sr1, sr2 = self.get_occupied_as_list(), other.get_occupied_as_list()
        l1, l2 = len(sr1), len(sr2)
        i1, i2 = 0, 0
        while i1 < l1 and i2 < l2:
            (lx1, rx1), (lx2, rx2) = sr1[i1], sr2[i2]
            if rx1 < lx2:
                i1 += 1
            elif rx2 < lx1:
                i2 += 1
            else:
                res.add(max(lx1, lx2), min(rx1, rx2))
                if lx1 <= lx2:
                    i1 += 1
                else:
                    i2 += 1
        return res

    def get_min_occupied(self) -> int:
        return self.get_occupied_as_list()[0][0]

    def get_max_occupied(self) -> int:
        return self.get_occupied_as_list()[-1][1]

    def get_limits(self) -> Tuple[int, int]:
        return self.get_min_occupied(), self.get_max_occupied()

    def get_span(self) -> int:
        return self.get_max_occupied() - self.get_min_occupied() + 1

    def get_total_occupied(self) -> int:
        return sum([rx - lx + 1 for lx, rx in self.get_occupied_as_list()])

    def get_total_available(self) -> int:
        return sum([rx - lx + 1 for lx, rx in self.get_available_as_list()])


class SetRange2D:

    def __init__(self, fill_border: str = "O", fill_values: str = "#", fill_void: str = " "):
        self._grid: Dict[int, SetRange1D] = dict()

        self.fill_border = fill_border
        self.fill_values = fill_values
        self.fill_void = fill_void

    def add(self, y: int, lx: int, rx: int) -> SetRange2D:
        if y in self._grid:
            self._grid[y].add(lx, rx)
        else:
            self._grid[y] = SetRange1D(lx, rx)
        return self

    def get(self, y: int) -> SetRange1D:
        return self._grid.get(y)

    def __invert__(self) -> SetRange2D:
        res = SetRange2D()

        _lim = self.get_limits()
        for y in range(_lim.y0, _lim.y1 + 1):
            res._grid[y] = self._grid[y].copy()

            res.add(y, _lim.x0-1, _lim.x0-1)
            res.add(y, _lim.x1+1, _lim.x1+1)

            res._grid[y] = res._grid[y].get_available()

        return res

    def get_min_y(self) -> int:
        return min(self._grid.keys())

    def get_max_y(self) -> int:
        return max(self._grid.keys())

    def get_min_x(self) -> int:
        return min(sr.get_min_occupied() for sr in self._grid.values())

    def get_max_x(self) -> int:
        return max(sr.get_max_occupied() for sr in self._grid.values())

    def get_limits(self) -> Limits:
        return Limits(self.get_min_y(), self.get_min_x(), self.get_max_y(), self.get_max_x())

    def get_size(self) -> Tuple[int, int]:
        _gl = self.get_limits()
        return _gl.y1 - _gl.y0 + 1, _gl.x1 - _gl.x0 + 1

    def get_total_occupied(self) -> int:
        return sum(self._grid[y].get_total_occupied() for y in range(self.get_min_y(), self.get_max_y() + 1))

    def flood_fill_as_str_table(self, outline: bool = True) -> List[str]:
        # change definitions to perform flood fill
        _fb, _fv, _fd, self.fill_border, self.fill_void, self.fill_values = self.fill_border, self.fill_void, self.fill_values, ".", ".", "#"

        # convert SetRange2D into list[list[char]] (outline ranges)
        res_table = [list(row) for row in str(self).split("\n")]

        # flood fill table
        len_y, len_x = len(res_table), len(res_table[0])
        visited, _queue = set(), {(0, 0)}
        while _queue:
            p = _queue.pop()
            if p not in visited:
                visited.add(p)
                y, x = p
                if res_table[y][x] == ".":
                    res_table[y][x] = " "
                    if y+1 < len_y:
                        _queue.add((y+1, x))
                    if x+1 < len_x:
                        _queue.add((y, x+1))
                    if y-1 > 0:
                        _queue.add((y-1, x))
                    if x-1 > 0:
                        _queue.add((y, x-1))

        # replace inner space "." with "#" if not outlined
        if outline:
            res_table = ["".join(row[1:-1]) for row in res_table[1:-1]]
        else:
            res_table = ["".join(row[1:-1]).replace(".", "#") for row in res_table[1:-1]]

        # rollback definitions
        self.fill_border, self.fill_void, self.fill_values = _fb, _fv, _fd

        return res_table

    def create_from_str_table(self, y0: int, x0: int, _table: List[str], char_pattern: str = "#+") -> SetRange2D:
        res = SetRange2D()
        for y, row in enumerate(_table):
            for g in re.finditer(char_pattern, row):
                res.add(y0 + y, x0 + g.span(0)[0], x0 + g.span(0)[1]-1)
        return res

    def flood_fill(self) -> SetRange2D:
        return self.create_from_str_table(self.get_min_y(), self.get_min_x(), self.flood_fill_as_str_table(outline=False), "#+")

    def __str__(self):
        """Will create an outline border around if self.fill_border defined with a char"""
        _lim = self.get_limits()

        # create first row as border, if self.fill_border defined
        res = self.fill_border * (_lim.x1 - _lim.x0 + 3) + "\n" if self.fill_border else ""

        for curr_y in range(_lim.y0, _lim.y1 + 1):
            # add border as beginning of row
            res += self.fill_border

            # fill row with chars defined for "fill_void" and "fill_values"
            _gy = self._grid[curr_y]
            _lx = _lim.x0
            for lx, rx in _gy:
                res += self.fill_void * (lx - _lx)
                res += self.fill_values * (rx - lx + 1)
                _lx = rx+1

            # fill empty space until the end, and add border if defined
            res += self.fill_void * (_lim.x1 - _lx + 1) + f"{self.fill_border}\n"

        # create last row as border, if self.fill_border defined
        if self.fill_border:
            res += self.fill_border * (_lim.x1 - _lim.x0 + 3) + "\n"

        return res[:-1]
