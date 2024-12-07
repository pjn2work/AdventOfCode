from typing import Tuple, List, Set

from utilities import time_duration


class OutOfBounds(Exception):
    pass


class Data:
    moves = [
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0),
    ]

    def __init__(self):
        self.puzzle: List[str] = []
        self.move: int = 0
        self.pos: Tuple[int, int] = (0, 0)

    def is_out_of_bounds(self, x: int, y: int) -> bool:
        return x < 0 or y < 0 or x >= len(self.puzzle[0]) or y >= len(self.puzzle)

    def change_move(self):
        self.move = (self.move + 1) % len(self.moves)

    def get_next_position(self, x: int, y: int) -> Tuple[int, int]:
        inc_x, inc_y = self.moves[self.move]
        return x + inc_x, y + inc_y

    def next_step(self, x: int, y: int) -> Tuple[int, int]:
        _x, _y = self.get_next_position(x, y)

        if self.is_out_of_bounds(_x, _y):
            raise OutOfBounds(f"{_x=}, {_y=}")

        if self.puzzle[_y][_x] == "#":
            self.change_move()
            return self.next_step(x, y)

        return _x, _y


@time_duration
def parse() -> Data:
    data: Data = Data()
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            data.puzzle.append(line)
            if "^" in line:
                data.pos = (line.find("^"), len(data.puzzle))
    return data


@time_duration
def part1(data: Data) -> int:
    initial_pos = x, y = data.pos
    seen: Set[Tuple[int, int]] = {(x, y)}

    try:
        while True:
            x, y = data.next_step(x, y)
            seen.add((x, y))
    except OutOfBounds:
        pass

    # reset
    data.pos = initial_pos
    data.move = 0

    return len(seen)


@time_duration
def part2(data: Data) -> int:
    x, y = data.pos
    seen: Set[Tuple[int, int, int]] = {(x, y, data.move)}
    blocks: Set[Tuple[int, int]] = set()

    try:
        while True:
            x, y = data.next_step(x, y)
            seen.add((x, y, data.move))

            block_pos = data.get_next_position(x, y)
            if not data.is_out_of_bounds(*block_pos) and data.puzzle[block_pos[0]][block_pos[1]] != "#":
                _move = data.move

                try:
                    _x, _y = x, y
                    data.change_move()
                    steps_seen = set()
                    while True:
                        sp = (_x, _y, data.move)
                        if sp in seen or sp in steps_seen:
                            blocks.add(block_pos)
                            break
                        steps_seen.add(sp)
                        _x, _y = data.next_step(_x, _y)
                except OutOfBounds:
                    pass

                data.move = _move
    except OutOfBounds:
        pass

    print(blocks)
    return len(blocks)


@time_duration
def run_all():
    data = parse()

    p1 = part1(data)
    p2 = part2(data)  # not working yet

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
