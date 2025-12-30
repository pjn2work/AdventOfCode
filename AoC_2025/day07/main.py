import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utilities import time_duration


@time_duration
def parse() -> list:
    with open("input.txt", mode="r", encoding="utf-8") as f:
        return [list(line.strip()) for line in f]


@time_duration
def part1(l1: list) -> int:
    len_x = len(l1[0]) - 1
    total = 0
    for y, line in enumerate(l1):
        for x, value in enumerate(line):
            if value == "S":
                l1[y+1][x] = "|"
            elif value == "^":
                if l1[y-1][x] == "|":
                    total += 1
                    if x > 0:
                        l1[y][x-1] = "|"
                    if x < len_x:
                        l1[y][x+1] = "|"
            elif y > 0 and value == "." and l1[y-1][x] == "|":
                l1[y][x] = "|"
    return total


@time_duration
def part2(l1: list) -> int:
    len_x = len(l1[0]) - 1
    totals = [
        [0 for _ in range(len(row))]
        for row in l1
    ]
    for y, line in enumerate(l1):
        for x, value in enumerate(line):
            if value == "S":
                totals[y+1][x] = 1
            elif value == "^":
                if l1[y-1][x] == "|":
                    if x > 0:
                        totals[y][x-1] += totals[y-1][x]
                    if x < len_x:
                        totals[y][x+1] += totals[y-1][x]
            elif y > 0:
                totals[y][x] += totals[y-1][x]

    return sum(totals[-1])


@time_duration
def run_all():
    l1 = parse()

    p1 = part1(l1)
    p2 = part2(l1)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
