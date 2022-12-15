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


class MapRange1D:
    def __init__(self):
        self.map_range: list[tuple[int, int]] = []

    @staticmethod
    def __assert_other(other):
        assert isinstance(other, MapRange1D), f"other not of type <class MapRange1D> but {type(other)}"

    def __merge_if_overlap(self):
        idx = 0
        while idx < len(self.map_range)-1:
            (lx1, rx1), (lx2, rx2) = self.map_range[idx], self.map_range[idx + 1]
            if rx1 >= lx2:
                self.map_range[idx] = (lx1, max(rx1, rx2))
                del self.map_range[idx + 1]
            else:
                idx += 1

    def add(self, lx: int, rx: int) -> MapRange1D:
        mr = self.get_occupied()
        lx, rx = min(lx, rx), max(lx, rx)
        for i, (lx2, rx2) in enumerate(mr):
            if rx+1 < lx2 or lx-1 > rx2:
                continue
            mr[i] = (min(lx2, lx), max(rx2, rx))
            self.__merge_if_overlap()
            return self

        mr.append((lx, rx))
        mr.sort()
        return self

    def subtract(self, lx: int, rx: int) -> MapRange1D:
        changed = False
        lx, rx = min(lx, rx), max(lx, rx)
        idx, mr = 0, self.get_occupied()
        while idx < len(mr):
            lx1, rx1 = mr[idx]
            if lx1 > rx:
                break

            it = get_intersect_type(lx1, rx1, lx, rx)
            if it == INTERSECT_NONE:
                idx += 1
            elif it == INTERSECT_ALL:
                del mr[idx]
            elif it == INTERSECT_LEFT:
                mr[idx] = (rx+1, rx1)
                idx += 1
            elif it == INTERSECT_RIGHT:
                mr[idx] = (lx1, lx-1)
                idx += 1
            else:   # MIDDLE
                changed = True
                mr[idx] = (lx1, lx-1)
                self.add(rx+1, rx1)
                idx += 1

        if changed:
            mr.sort()

        return self

    def copy(self) -> MapRange1D:
        res = MapRange1D()
        res.map_range = self.map_range.copy()
        return res

    def __add__(self, other: MapRange1D) -> MapRange1D:
        self.__assert_other(other)
        res = self.copy()
        for lx, rx in other.get_occupied():
            res.add(lx, rx)
        return res

    def __sub__(self, other: MapRange1D):
        self.__assert_other(other)
        res = self.copy()
        for lx, rx in other.get_occupied():
            res.subtract(lx, rx)
        return res

    def __invert__(self):
        res = MapRange1D()
        res.map_range = self.get_available()
        return res

    def get_occupied(self) -> list[tuple[int, int]]:
        return self.map_range
    
    def get_available(self) -> list[tuple[int, int]]:
        res = []
        if len(self.map_range) > 1:
            for (_, rx1), (lx2, _) in zip(self.map_range, self.map_range[1:]):
                res.append((rx1+1, lx2-1))
        return res

    def get_inner_join(self, other: MapRange1D) -> MapRange1D:
        self.__assert_other(other)
        res = MapRange1D()
        mr1, mr2 = self.get_occupied(), other.get_occupied()
        l1, l2 = len(mr1), len(mr2)
        i1, i2 = 0, 0
        while i1 < l1 and i2 < l2:
            (lx1, rx1), (lx2, rx2) = mr1[i1], mr2[i2]
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

    def get_limits(self):
        return self.get_min_occupied(), self.get_max_occupied()

    def get_total_occupied(self) -> int:
        return sum([rx-lx+1 for lx, rx in self.get_occupied()])

    def get_total_available(self) -> int:
        return sum([rx-lx+1 for lx, rx in self.get_available()])
