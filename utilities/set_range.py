from __future__ import annotations


INTERSECT_NONE = 0
INTERSECT_LEFT = 1
INTERSECT_MIDDLE = 2
INTERSECT_RIGHT = 3
INTERSECT_ALL = 4


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
        self.set_range: list[tuple[int, int]] = []
        if lx is not None and rx is not None:
            self.add(lx, rx)
        self._current_index = 0

    @staticmethod
    def __assert_other(other):
        assert isinstance(other, SetRange1D), f"other not of type <class MapRange1D> but {type(other)}"

    def __merge_if_overlap(self):
        idx = 0
        while idx < len(self.set_range) - 1:
            (lx1, rx1), (lx2, rx2) = self.set_range[idx], self.set_range[idx + 1]
            if rx1 + 1 >= lx2:
                self.set_range[idx] = (lx1, max(rx1, rx2))
                del self.set_range[idx + 1]
            else:
                idx += 1

    def add(self, lx: int, rx: int) -> SetRange1D:
        sr = self.get_occupied()
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

    def sub(self, lx: int, rx: int) -> SetRange1D:
        lx, rx = min(lx, rx), max(lx, rx)
        idx, sr = 0, self.get_occupied()
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
        res.set_range = self.set_range.copy()
        return res

    def clear(self):
        self.set_range.clear()

    def __add__(self, other: SetRange1D) -> SetRange1D:
        self.__assert_other(other)
        res = self.copy()
        for lx, rx in other.get_occupied():
            res.add(lx, rx)
        return res

    def __sub__(self, other: SetRange1D):
        self.__assert_other(other)
        res = self.copy()
        for lx, rx in other.get_occupied():
            res.sub(lx, rx)
        return res

    def __invert__(self):
        res = SetRange1D()
        res.set_range = self.get_available()
        return res

    def __lshift__(self, n: int):
        for i in range(len(self.set_range)):
            lx, rx = self.set_range[i]
            self.set_range[i] = (lx - n, rx - n)
        return self

    def __rshift__(self, n: int):
        for i in range(len(self.set_range)):
            lx, rx = self.set_range[i]
            self.set_range[i] = (lx + n, rx + n)
        return self

    def __bool__(self):
        return bool(self.set_range)

    def __eq__(self, other):
        self.__assert_other(other)
        return self.get_occupied() == other.get_occupied()

    def __iter__(self):
        for o in self.get_occupied():
            yield o

    def __next__(self):
        o = self.get_occupied()
        if self._current_index < len(o):
            self._current_index += 1
            return o[self._current_index - 1]
        self._current_index = 0
        raise StopIteration

    def __str__(self):
        return str(self.get_occupied())

    def __repr__(self):
        return str(self.get_occupied())

    def get_occupied(self) -> list[tuple[int, int]]:
        return self.set_range

    def get_available(self) -> list[tuple[int, int]]:
        res = []
        if len(self.set_range) > 1:
            for (_, rx1), (lx2, _) in zip(self.set_range, self.set_range[1:]):
                res.append((rx1 + 1, lx2 - 1))
        return res

    def get_inner_join(self, other: SetRange1D) -> SetRange1D:
        self.__assert_other(other)
        res = SetRange1D()
        sr1, sr2 = self.get_occupied(), other.get_occupied()
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

    def is_position_occupied(self, x: int):
        for lx, rx in self.get_occupied():
            if lx <= x <= rx:
                return True
        return False

    def is_position_available(self, x: int):
        return not self.is_position_occupied(x)

    def get_min_occupied(self) -> int:
        return self.get_occupied()[0][0]

    def get_max_occupied(self) -> int:
        return self.get_occupied()[-1][1]

    def get_limits(self) -> tuple[int, int]:
        return self.get_min_occupied(), self.get_max_occupied()

    def get_total_occupied(self) -> int:
        return sum([rx - lx + 1 for lx, rx in self.get_occupied()])

    def get_total_available(self) -> int:
        return sum([rx - lx + 1 for lx, rx in self.get_available()])
