import sys
sys.path.append("../..")
from utilities import time_duration

from collections import namedtuple
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
import re


Cube = namedtuple("Cube", "x, y, z")
Brick = List[Cube]


@dataclass
class Puzzle:
    bricks: List[Brick]
    busy_cubes: Dict[Cube, int]

    def _move_brick_down(self, brick_id: int) -> bool:
        # shift brick down
        _brick_down: Brick = []
        for cube in self.bricks[brick_id]:
            _cube_down = Cube(cube.x, cube.y, cube.z - 1)
            if cube.z > 1 and (_cube_down not in self.busy_cubes or self.busy_cubes[_cube_down] == brick_id):
                _brick_down.append(_cube_down)
            else:
                return False

        # remove old cubes for this brick
        for cube in self.bricks[brick_id]:
            del self.busy_cubes[cube]

        # add new cubes for this brick
        for cube in _brick_down:
            self.busy_cubes[cube] = brick_id

        # replace old brick cubes with new one
        self.bricks[brick_id] = _brick_down

        return True

    def settle_bricks(self, removed_brick: Set) -> int:
        bricks_moved = set()
        moved = True
        while moved:
            moved = False
            for brick_id in range(len(self.bricks)):
                if brick_id not in removed_brick and self._move_brick_down(brick_id):
                    moved = True
                    bricks_moved.add(brick_id)
        return len(bricks_moved)

    def _copy(self):
        return Puzzle(self.bricks.copy(), self.busy_cubes.copy())

    def _remove_brick(self, brick_id: int):
        # delete all cubes for that brick
        for cube in self.bricks[brick_id]:
            del self.busy_cubes[cube]

        # set that position with nothing
        self.bricks[brick_id] = None

        return self

    def remove_brick_causes_how_many_moves(self, brick_id: int) -> int:
        return self._copy()._remove_brick(brick_id).settle_bricks({brick_id})


@time_duration
def parse() -> Puzzle:
    num = re.compile(r"\d+")

    puzzle = Puzzle([], dict())

    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            l, r = line.strip().split("~")
            l = Cube(*[int(n.group()) for n in num.finditer(l)])
            r = Cube(*[int(n.group()) for n in num.finditer(r)])

            brick = []
            brick_id = len(puzzle.bricks)
            for z in range(l.z, r.z+1):
                for y in range(l.y, r.y+1):
                    for x in range(l.x, r.x+1):
                        c = Cube(x, y, z)
                        brick.append(c)
                        puzzle.busy_cubes[c] = brick_id

            puzzle.bricks.append(brick)

    return puzzle


# part 1 & 2 ----------------

@time_duration
def solve(puzzle: Puzzle) -> Tuple[int, int]:
    # settle puzzle first
    puzzle.settle_bricks(set())

    # remove bricks, one by one
    p1 = p2 = 0
    for brick_id in range(len(puzzle.bricks)):
        tm = puzzle.remove_brick_causes_how_many_moves(brick_id)
        if tm:
            p2 += tm
        else:
            p1 += 1

    return p1, p2


@time_duration
def run_all():
    puzzle = parse()

    p1, p2 = solve(puzzle)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
