from typing import Tuple, List

from utilities import time_duration


Data = List[Tuple[int, ...]]


@time_duration
def parse() -> Data:
    data: Data = []
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            report = line.strip().split(" ")
            data.append(tuple(map(int, report)))
    return data


def _is_safe_report(report: Tuple[int, ...]) -> bool:
    step = report[1] - report[0]
    _min, _max = (-3, -1) if step < 0 else (1, 3)
    is_safe = lambda v: _min <= v <= _max

    for v1, v2 in zip(report, report[1:]):
        if not is_safe(v2 - v1):
            return False
    return True


@time_duration
def part1(data: Data) -> int:
    result = 0
    for report in data:
        if _is_safe_report(report):
            result += 1
    return result


@time_duration
def part2(data: Data) -> int:
    result = 0
    for report in data:
        if _is_safe_report(report):
            result += 1
        else:
            for pos in range(len(report)):
                if _is_safe_report(report[0:pos] + report[pos + 1:]):
                    result += 1
                    break
    return result


@time_duration
def run_all():
    data = parse()

    p1 = part1(data)
    p2 = part2(data)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
