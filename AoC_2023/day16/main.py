import sys

sys.path.append("../..")
from utilities import time_duration

from typing import List, Tuple


Data = List[str]


@time_duration
def parse() -> Data:
    data = []
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            data.append(line.strip())
    return data


MOVES = {
    ">": (0, 1),
    "<": (0, -1),
    "v": (1, 0),
    "^": (-1, 0),
}


class Beam:
    def __init__(self, y: int, x: int, direction: str):
        self.y = y
        self.x = x
        self.direction = direction

    def move(self):
        self.y += MOVES[self.direction][0]
        self.x += MOVES[self.direction][1]
        return self

    def apply_tile_and_move(self, tile: str) -> List["Beam"]:
        if self.direction == ">":
            if tile == "\\":
                self.direction = "v"
            if tile == "/":
                self.direction = "^"
            elif tile == "|":
                return [Beam(self.y-1, self.x, "^"), Beam(self.y+1, self.x, "v")]
        elif self.direction == "<":
            if tile == "\\":
                self.direction = "^"
            if tile == "/":
                self.direction = "v"
            elif tile == "|":
                return [Beam(self.y-1, self.x, "^"), Beam(self.y+1, self.x, "v")]
        elif self.direction == "v":
            if tile == "\\":
                self.direction = ">"
            if tile == "/":
                self.direction = "<"
            elif tile == "-":
                return [Beam(self.y, self.x-1, "<"), Beam(self.y, self.x+1, ">")]
        elif self.direction == "^":
            if tile == "\\":
                self.direction = "<"
            if tile == "/":
                self.direction = ">"
            elif tile == "-":
                return [Beam(self.y, self.x-1, "<"), Beam(self.y, self.x+1, ">")]
        return [self.move()]

    def as_tuple(self) -> Tuple[int, int, "str"]:
        return self.y, self.x, self.direction


def is_inbound(data: Data, beam: Beam) -> bool:
    return 0 <= beam.y < len(data) and 0 <= beam.x < len(data[0])


def calc_pos_visited(data: Data, beam: Beam) -> int:
    visited = {beam.as_tuple()}
    moves = beam.apply_tile_and_move(data[beam.y][beam.x])

    while moves:
        beam = moves.pop(0)
        bt = beam.as_tuple()
        if is_inbound(data, beam) and bt not in visited:
            # save position and direction
            visited.add(bt)

            # apply tile effect and move accordingly
            beams = beam.apply_tile_and_move(data[beam.y][beam.x])
            if beams:
                moves.extend(beams)

    return len(set((y,x) for y,x,_ in visited))


# part 1 ----------------

@time_duration
def part1(data: Data) -> int:
    return calc_pos_visited(data, Beam(0, 0, ">"))


# part 2 ----------------

@time_duration
def part2(data: Data) -> int:
    m = 0
    lx, ly = len(data), len(data[0])
    for y in range(ly):
        m = max(m, calc_pos_visited(data, Beam(y, 0, ">")))
        m = max(m, calc_pos_visited(data, Beam(y, lx-1, "<")))
    for x in range(lx):
        m = max(m, calc_pos_visited(data, Beam(0, x, "v")))
        m = max(m, calc_pos_visited(data, Beam(ly-1, x, "^")))
    return m


@time_duration
def run_all():
    data = parse()

    p1 = part1(data)
    p2 = part2(data)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
