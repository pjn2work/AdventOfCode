
class MapRange1D:
    def __init__(self):
        self.map_range: list[tuple[int, int]] = []

    def add(self, lx: int, rx: int):
        def merge_if_overlap():
            idx = 0
            while idx < len(self.map_range)-1:
                (lx1, rx1), (lx2, rx2) = self.map_range[idx], self.map_range[idx + 1]
                if rx1 >= lx2:
                    self.map_range[idx] = (lx1, max(rx1, rx2))
                    del self.map_range[idx + 1]
                else:
                    idx += 1
    
        lx, rx = min(lx, rx), max(lx, rx)
        for i, (lx2, rx2) in enumerate(self.map_range):
            if rx+1 < lx2 or lx-1 > rx2:
                continue
            self.map_range[i] = (min(lx2, lx), max(rx2, rx))
            self.map_range.sort()
            merge_if_overlap()
            return self

        self.map_range.append((lx, rx))
        self.map_range.sort()
        return self

    def get_occupied(self) -> list[tuple[int, int]]:
        return self.map_range
    
    def get_available(self) -> list[tuple[int, int]]:
        res = []
        if len(self.map_range) > 1:
            for (_, rx1), (lx2, _) in zip(self.map_range, self.map_range[1:]):
                res.append((rx1+1, lx2-1))
        return res

    def is_position_occupied(self, x: int):
        for lx, rx in self.get_occupied():
            if lx <= x <= rx:
                return True
        return False

    def get_min_occupied(self) -> int:
        return self.map_range[0][0]

    def get_max_occupied(self) -> int:
        return self.map_range[-1][1]

    def get_total_occupied(self) -> int:
        return sum([rx-lx+1 for lx, rx in self.get_occupied()])

    def get_total_available(self) -> int:
        return sum([rx-lx+1 for lx, rx in self.get_available()])
