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
        self._set_range: list[tuple[int, int]] = []
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
            for lx, rx in other.get_occupied():
                self.add(lx, rx)
        return self

    def __isub__(self, other: SetRange1D) -> SetRange1D:
        if isinstance(other, int):
            self.sub(other, other)
        elif isinstance(other, (tuple, list)) and len(other) == 2:
            self.sub(other[0], other[1])
        else:
            self.__assert_other(other)
            for lx, rx in other.get_occupied():
                self.sub(lx, rx)
        return self

    def __add__(self, other: SetRange1D) -> SetRange1D:
        return self.copy().__iadd__(other)

    def __sub__(self, other: SetRange1D) -> SetRange1D:
        return self.copy().__isub__(other)

    def __invert__(self) -> SetRange1D:
        res = SetRange1D()
        res._set_range = self.get_available()
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
        return self.get_occupied() == other.get_occupied()

    def __contains__(self, item) -> bool:
        if isinstance(item, int):
            for lx, rx in self.get_occupied():
                if lx <= item <= rx:
                    return True
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            lx2, rx2 = item
            for lx, rx in self.get_occupied():
                if lx <= lx2 <= rx2 <= rx:
                    return True
        elif isinstance(item, SetRange1D):
            sr1 = self.get_occupied()
            l1, i1 = len(sr1), 0
            if l1 == 0:
                return False

            lx1, rx1 = sr1[i1]
            for lx2, rx2 in item.get_occupied():
                while rx1 < lx2:
                    i1 += 1
                    if i1 == l1:
                        return False
                    lx1, rx1 = sr1[i1]

                if not lx1 <= lx2 <= rx2 <= rx1:
                    return False
            return True

        return False

    def __iter__(self) -> tuple[int, int]:
        for o in self.get_occupied():
            yield o

    def __next__(self) -> tuple[int, int]:
        o = self.get_occupied()
        if self._current_index < len(o):
            self._current_index += 1
            return o[self._current_index - 1]
        self._current_index = 0
        raise StopIteration

    def __str__(self) -> str:
        return str(self.get_occupied())

    def __repr__(self) -> str:
        return str(self.get_occupied())

    def get_occupied(self) -> list[tuple[int, int]]:
        return self._set_range

    def get_available(self) -> list[tuple[int, int]]:
        res = []
        if len(self._set_range) > 1:
            for (_, rx1), (lx2, _) in zip(self._set_range, self._set_range[1:]):
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
