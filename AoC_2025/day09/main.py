import sys
import os
from itertools import combinations

# Add project root to sys.path
CWD = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(CWD, "../..")))

from utilities import time_duration, Polygon


Point = tuple[int, int]


@time_duration
def parse() -> list[Point]:
    with open(os.path.join(CWD, "input.txt"), mode="r", encoding="utf-8") as f:
        return [tuple(map(int, line.strip().split(","))) for line in f]


@time_duration
def part1(l1: list[Point]) -> int:
    all_areas = [abs(p1[0] - p2[0] + 1) * abs(p1[1] - p2[1] + 1) for p1, p2 in combinations(l1, 2)]
    return max(all_areas)


@time_duration
def part2(l1: list[Point]) -> int:
    poly = Polygon(l1)
    possible_rectangles = [Polygon([p1, (p1[0], p2[1]), p2, (p2[0], p1[1])]) for p1, p2 in combinations(l1, 2)]

    max_area = 0
    for rectangle_poly in possible_rectangles:
        area = rectangle_poly.get_grid_area()
        is_rectangle_inside_poly = poly.get_polygon_relationship(rectangle_poly) == 2
        if area > max_area and is_rectangle_inside_poly:
            max_area = max(max_area, area)
    return max_area


@time_duration
def run_all():
    l1 = parse()

    p1 = part1(l1)
    p2 = part2(l1)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
