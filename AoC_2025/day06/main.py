import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utilities import time_duration


@time_duration
def parse() -> list:
    with open("input.txt", mode="r", encoding="utf-8") as f:
        return [line for line in f]


@time_duration
def part1(l1: list) -> int:
    l1 = [line.strip().split() for line in l1]
    totals = [1 if op == "*" else 0 for op in l1[-1]]
    for y, line in enumerate(l1[:-1]):
        for x, value in enumerate(line):
            op = l1[-1][x]
            totals[x] = eval(f"{totals[x]} {op} {value}")
    return sum(totals)


@time_duration
def part2(l1: list) -> int:
    totals = []
    for x, op in enumerate(l1[-1]):
        if op != " ":
            operation = op
            total = 1 if operation == "*" else 0
        
        column = "".join([line[x] for line in l1[:-1]])
        if column.strip():
            for value in column.split():
                total = eval(f"{total} {operation} {value}")
        else:
            totals.append(total)
    totals.append(total)
    return sum(totals)


@time_duration
def run_all():
    l1 = parse()

    p1 = part1(l1)
    p2 = part2(l1)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
