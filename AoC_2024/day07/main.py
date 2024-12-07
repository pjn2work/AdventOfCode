from typing import Tuple, List

from utilities import time_duration


Data = List[Tuple[int, Tuple[int, ...]]]


@time_duration
def parse() -> Data:
    data = []
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            total, numbers = line.strip().split(": ")
            data.append((int(total), tuple(map(int, numbers.split(" ")))))
    return data


@time_duration
def part1(data: Data) -> int:
    def _compute(total: int, values: Tuple[int, ...], acc: int = 0) -> bool:
        if len(values) == 0:
            return total == acc
        if acc > total:
            return False
        return _compute(total, values[1:], acc + values[0]) or \
            _compute(total, values[1:], (acc or 1) * values[0])

    result = [
        equation[0]
        for equation in data
        if _compute(*equation)
    ]
    return sum(result)


@time_duration
def part2(data: Data) -> int:
    def _compute(total: int, values: Tuple[int, ...], acc: int = 0) -> bool:
        if len(values) == 0:
            return total == acc
        if acc > total:
            return False
        return _compute(total, values[1:], acc + values[0]) or \
            _compute(total, values[1:], (acc or 1) * values[0]) or \
            _compute(total, values[1:], int(str(acc) + str(values[0])))

    result = [
        equation[0]
        for equation in data
        if _compute(*equation)
    ]
    return sum(result)


@time_duration
def run_all():
    data = parse()

    p1 = part1(data)
    p2 = part2(data)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
