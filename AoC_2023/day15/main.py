import sys

sys.path.append("../..")
from utilities import time_duration

from typing import List


Data = List[str]


@time_duration
def parse() -> Data:
    with open("input.txt", mode="r", encoding="utf-8") as f:
        _data = f.readline().strip().split(",")
    return _data


def hash_str(s: str) -> int:
    res = 0
    for c in s:
        res = (res + ord(c)) * 17 % 256
    return res


# part 1 ----------------

@time_duration
def part1(data: Data) -> int:
    return sum(hash_str(s) for s in data)


# part 2 ----------------

@time_duration
def part2(data: Data) -> int:
    hashmap = {i: dict() for i in range(256)}
    for s in data:
        if s.endswith("-"):
            label = s[:-1]
            box = hash_str(label)
            if label in hashmap[box]:
                del hashmap[box][label]
        else:
            label, value = s.split("=")
            box = hash_str(label)
            hashmap[box][label] = int(value)

    res = 0
    for box in range(256):
        for idx, value in enumerate(hashmap[box].values()):
            res += (box+1) * (idx+1) * value

    return res


@time_duration
def all():
    data = parse()

    p1 = part1(data)
    p2 = part2(data)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    all()
