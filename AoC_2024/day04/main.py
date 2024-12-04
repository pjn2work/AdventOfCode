from typing import Tuple, List

from utilities import time_duration


class Data:
    def __init__(self):
        self.puzzle = []
        self.width = 0
        self.height = 0

    def is_outbounds(self, x: int, y: int) -> bool:
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def find_xmas(self, x: int, y: int, seen: list):
        if self.puzzle[y][x] != "X":
            return

        moves = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
        for inc_x, inc_y in moves:
            end_pos_x, end_pos_y = (x + inc_x*3, y + inc_y*3)
            if self.is_outbounds(end_pos_x, end_pos_y) or (end_pos_x, end_pos_y) in seen:
                continue

            _x, _y = x, y
            for ch in "MAS":
                _x += inc_x
                _y += inc_y
                if self.puzzle[_y][_x] != ch:
                    break
            else:
                seen.append((x, y))

    def find_x_mas(self, x: int, y: int, seen: list):
        if self.puzzle[y][x] != "A":
            return

        moves = [
            [(-1, -1), (1, 1)],
            [(1, -1), (-1, 1)]
        ]

        found = 0
        for move in moves:
            find_chars = ["M", "S"]
            for inc_x, inc_y in move:
                _x = x + inc_x
                _y = y + inc_y
                ch = self.puzzle[_y][_x]
                if ch in find_chars:
                    find_chars.remove(ch)

            if len(find_chars) == 0:
                found += 1

        if found == 2:
            seen.append((x, y))


@time_duration
def parse() -> Data:
    data: Data = Data()
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            v = line.strip()
            data.puzzle.append(v)
    data.width = len(data.puzzle[0])
    data.height = len(data.puzzle)
    return data


@time_duration
def part1(data: Data) -> int:
    seen = []
    for y in range(data.height):
        for x in range(data.width):
            data.find_xmas(x, y, seen)
    return len(seen)


@time_duration
def part2(data: Data) -> int:
    seen = []
    for y in range(1, data.height - 1):
        for x in range(1, data.width - 1):
            data.find_x_mas(x, y, seen)
    return len(seen)


@time_duration
def run_all():
    data = parse()

    p1 = part1(data)
    p2 = part2(data)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
