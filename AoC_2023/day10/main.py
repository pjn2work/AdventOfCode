import sys
sys.path.append("../..")
from utilities import time_duration

from typing import List, Tuple
import re


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def copy(self) -> "Point":
        return Point(self.x, self.y)

    def as_tuple(self) -> Tuple[int, int]:
        return self.x, self.y
    
    def move(self, move):
        if isinstance(move, str):
            self.move(MOVES[move])
        else:
            self.x += move.x
            self.y += move.y


class Step:
    def __init__(self, pos: Point, move: str, visited: List):
        self.pos = pos
        self.direction = move
        self.visited = visited


MOVES = {
    "^": Point(x=0, y=-1),
    "v": Point(x=0, y=1),
    ">": Point(x=1, y=0),
    "<": Point(x=-1, y=0)
}
ALLOWED_MOVES_TO = {
    "F": {"<": "v", "^": ">"}, # "F" - who comes form "<" can go "V", who comes form "^" can go ">"
    "L": {"<": "^", "v": ">"},
    "J": {">": "^", "v": "<"},
    "7": {">": "v", "^": "<"},
    "-": {">": ">", "<": "<"},
    "|": {"^": "^", "v": "v"}
}
"""
map loop
F-7
| |
L-J
"""

class Map:
    grid: List[List[str]]

    def __init__(self):
        self.grid = []
        self.start = Point(0, 0)
        self.all_pos_visited = set()

    def append_map(self, row: str):
        if "S" in row:
            self.start = Point(row.index("S"), len(self.grid))
        self.grid.append(list(row))

    def is_inside_map_bounds(self, pos: Point) -> bool:
        return 0 <= pos.y < len(self.grid) and 0 <= pos.x < len(self.grid[pos.y])
    
    def get_tile_at_position(self, pos: Point) -> str:
        if self.is_inside_map_bounds(pos):
            return self.grid[pos.y][pos.x]
        return ""

    def move_to_and_get_next_move(self, step: Step) -> bool:
        step.pos.move(step.direction)
        tile = self.get_tile_at_position(step.pos)

        if tile in ALLOWED_MOVES_TO:
            if step.direction in ALLOWED_MOVES_TO[tile] and step.pos not in step.visited:
                _visited = step.pos.as_tuple()
                self.all_pos_visited.add(_visited)
                step.visited.append(_visited)

                step.direction = ALLOWED_MOVES_TO[tile][step.direction]
                return True
        return False


@time_duration
def parse() -> Map:
    _map = Map()
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            _map.append_map(line.strip())
    return _map


# part 1 ----------------

@time_duration
def part1(_map: Map) -> int:
    _moves: List[Step] = [Step(_map.start.copy(), direction, []) for direction in MOVES]
    _max = 0
    while _moves:
        next_move = _moves.pop(0)
        if _map.move_to_and_get_next_move(next_move):
            _moves.append(next_move)
        else:
            _max = max(_max, len(next_move.visited))
    return round(_max / 2)


# part 2 ----------------

@time_duration
def part2(_map: Map) -> int:
    total_inside = 0
    for y, tiles in enumerate(_map.grid):
        # keep tiles for only visited path
        row = [v if (x, y) in _map.all_pos_visited else " " for x, v in enumerate(tiles)]

        # remove horizontals (LJ and FJ are even)
        row = "".join(row)
        row = re.sub(r"L-*7", "|", row)
        row = re.sub(r"L-*J", "||", row)
        row = re.sub(r"F-*7", "||", row)
        row = re.sub(r"F-*J", "|", row)

        # count " " that are inside a loop
        vertical = inside = 0
        for tile in row:
            if tile in " S" and vertical % 2 == 1:
                inside += 1
            elif tile in "F7LJ|":
                vertical += 1
        total_inside += inside

    return total_inside-1


@time_duration
def all():
    _map = parse()

    p1 = part1(_map)
    p2 = part2(_map)  # depends on part 1

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    all()
