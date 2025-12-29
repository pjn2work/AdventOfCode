import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utilities import time_duration, SetRange1D


@time_duration
def parse() -> tuple[list, list]:
    p1 = True
    l1, l2 = [], []
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                p1 = False
                continue
            if p1:
                l1.append(SetRange1D(*map(int, line.split("-"))))
            else:
                l2.append(int(line))

    return (l1, l2)


@time_duration
def part1(l1: list, l2: list) -> int:
    total = 0
    for ID in l2:
        for range1d in l1:
            if ID in range1d:
                total += 1
                break

    return total


@time_duration
def part2(l1: list) -> int:
    total = l1[0]
    for range1d in l1[1:]:
        total += range1d
    return total.get_total_occupied()



@time_duration
def run_all():
    l1, l2 = parse()

    p1 = part1(l1, l2)
    p2 = part2(l1)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
