from utilities import SetRange1D
from dataclasses import dataclass
import re


def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


@dataclass
class Puzzle:
    sensors: list[((int, int), int)]  # (y, x), radius
    beacons: set[(int, int)]          # (y, x)


def radius(x1, y1, x2, y2) -> int:
    return abs(x2-x1) + abs(y2-y1)


def read_input(line: str, p: Puzzle):
    sx, sy, bx, by = list(map(int, re.findall(r"-?\d+", line)))
    p.sensors.append(((sy, sx), radius(sx, sy, bx, by)))
    p.beacons.add((by, bx))


def count_beacons_in_row(p: Puzzle, y: int) -> int:
    return sum([1 for b in p.beacons if y == b[0]])


def sensor_span_on_y(sy, sx, r, y: int) -> tuple[int, int]:
    d = r - abs(sy-y)
    if d < 0:
        return None
    return sx-d, sx+d


def answer1(p: Puzzle, y: int) -> int:
    occupied_in_row = SetRange1D()
    for coord, r in p.sensors:
        if span := sensor_span_on_y(*coord, r, y):
            occupied_in_row.add(*span)
    return occupied_in_row.get_total_occupied() - occupied_in_row.get_total_available() - count_beacons_in_row(p, y)


def answer2(p: Puzzle, offset: int) -> str:
    p_pos, n_pos = [], []

    for s, r in p.sensors:
        n_pos.extend([s[1] + s[0] - r, s[1] + s[0] + r])
        p_pos.extend([s[1] - s[0] - r, s[1] - s[0] + r])

    pos, neg, tot_sensors = None, None, len(p.sensors)

    for i in range(2 * tot_sensors):
        for j in range(i + 1, 2 * tot_sensors):
            p1, p2 = p_pos[i], p_pos[j]
            if abs(p1 - p2) == 2:
                pos = min(p1, p2) + 1

            p1, p2 = n_pos[i], n_pos[j]
            if abs(p1 - p2) == 2:
                neg = min(p1, p2) + 1

    x, y = (pos + neg) // 2, (neg - pos) // 2
    return str(x * offset + y) + f" {x=} {y=}"


if __name__ == "__main__":
    puzzle = Puzzle(sensors=[], beacons=set())
    parser(read_input, p=puzzle)

    print("Answer 1:", answer1(puzzle, 2000000))
    print("Answer 2:", answer2(puzzle, 4000000))
