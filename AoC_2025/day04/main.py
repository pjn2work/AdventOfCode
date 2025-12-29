import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utilities import time_duration


@time_duration
def parse() -> list:
    with open("input.txt", mode="r", encoding="utf-8") as f:
        return [list(line.strip()) for line in f]


def get_adjacent_rolls(grid: list, x: int, y: int) -> list[str]:
    return [grid[_y][_x] for _y in range(max(0, y-1), min(y+2, len(grid))) for _x in range(max(0, x-1), min(x+2, len(grid[_y]))) if (_y, _x) != (y, x)]
    

@time_duration
def part1(l1: list) -> int:
    total = 0
    for y in range(len(l1)):
        for x in range(len(l1[y])):
            if l1[y][x] != "@":
                continue
            
            adjacent_rolls = get_adjacent_rolls(l1, x, y)
            if adjacent_rolls and adjacent_rolls.count("@") < 4:
                total += 1

    return total


@time_duration
def part2(l1: list) -> int:
    total = 0
    removed = True
    while removed:
        removed = False
        for y in range(len(l1)):
            for x in range(len(l1[y])):
                if l1[y][x] != "@":
                    continue

                adjacent_rolls = get_adjacent_rolls(l1, x, y)
                if adjacent_rolls and adjacent_rolls.count("@") < 4:
                    total += 1
                    l1[y][x] = "x"
                    removed = True

    return total


@time_duration
def run_all():
    l1 = parse()

    p1 = part1(l1)
    p2 = part2(l1)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
