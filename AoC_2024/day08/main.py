from typing import Tuple, List, Dict, Set, Callable
from collections import defaultdict
from utilities import time_duration


class Pos:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    def __add__(self, other):
        return Pos(self.y + other.y, self.x + other.x)

    def __sub__(self, other):
        return Pos(self.y - other.y, self.x - other.x)

    def to_tuple(self) -> Tuple[int, int]:
        return self.y, self.x


class Data:
    def __init__(self):
        self.puzzle: List[str] = []
        self.antennas: Dict[str, List[Pos]] = defaultdict(list)
        self.anti_nodes: Set[Pos] = set()

    def is_in_bounds(self, pos: Pos) -> bool:
        return 0 <= pos.y < len(self.puzzle) and 0 <= pos.x < len(self.puzzle[0])

    def is_empty(self, pos: Pos) -> bool:
        return self.puzzle[pos.y][pos.x] == "."

    def opposite_distance(self, p1: Pos, p2: Pos) -> List:
        r1 = p2 - p1 + p2
        r2 = p1 - p2 + p1
        return [r.to_tuple() for r in [r1, r2] if self.is_in_bounds(r)]

    def opposite_distance_propagated(self, p1: Pos, p2: Pos) -> List:
        d1, d2 = p2 - p1, p1 - p2
        anti_nodes = [p1, p2]
        for p, d in [(p2, d1), (p1, d2)]:
            pos = p + d
            while self.is_in_bounds(pos):
                if self.is_empty(pos):
                    anti_nodes.append(pos.to_tuple())
                pos += d
        return anti_nodes


@time_duration
def parse() -> Data:
    data = Data()
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for y, line in enumerate(f):
            line = line.strip()
            data.puzzle.append(line)

            # Save antennas positions
            for x, c in enumerate(line):
                if c != ".":
                    data.antennas[c].append(Pos(y, x))
    return data


def _find_anti_nodes(data: Data, func: Callable) -> int:
    anti_nodes = set()
    for antenna, positions in data.antennas.items():
        # find anti nodes for each pair of antennas
        for i, p1 in enumerate(positions[:-1]):
            for p2 in positions[i + 1:]:
                for anti_pos in func(p1, p2):
                    anti_nodes.add(anti_pos)
    return len(anti_nodes)


@time_duration
def part1(data: Data) -> int:
    return _find_anti_nodes(data, data.opposite_distance)


@time_duration
def part2(data: Data) -> int:
    return _find_anti_nodes(data, data.opposite_distance_propagated)


@time_duration
def run_all():
    data = parse()

    p1 = part1(data)
    p2 = part2(data)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
