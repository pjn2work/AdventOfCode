from collections import defaultdict
from typing import Dict, List, Tuple, Set

from utilities import time_duration


class Data:
    def __init__(self) -> None:
        self.before: Dict[int, Set] = defaultdict(set)
        self.pages_updates: List[Tuple[int]] = []

    def is_n_before_v(self, n: int, v: int) -> bool:
        return v in self.before[n]

    def page_must_be_before_seq(self, n: int, seq: Tuple[int]) -> bool:
        for v in seq:
            if not self.is_n_before_v(n, v):
                return False
        return True

    def is_correct_sequence(self, seq: Tuple[int]) -> bool:
        for i, page in enumerate(seq):
            if not self.page_must_be_before_seq(page, seq[i+1:]):
                return False
        return True

    def fix_sequence(self, seq: Tuple[int]) -> List[int]:
        result = [*seq]
        for i in range(len(seq)-1):
            for j in range(i+1, len(seq)):
                n = result[i]
                v = result[j]
                if not self.is_n_before_v(n, v):
                    result[i] = v
                    result[j] = n
        return result


@time_duration
def parse() -> Data:
    data: Data = Data()
    order_step = True
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if order_step:
                if line == "":
                    order_step = False
                    continue

                # Save page ordering rules
                v1, v2 = tuple(map(int, line.split("|")))
                data.before[v1].add(v2)
            else:
                # order of updates to be tested
                data.pages_updates.append(tuple(map(int, line.split(","))))
    return data


@time_duration
def part1(data: Data) -> int:
    middle: List[int] = [
        seq[len(seq) // 2]
        for seq in data.pages_updates
        if data.is_correct_sequence(seq)
    ]
    return sum(middle)


@time_duration
def part2(data: Data) -> int:
    middle: List[int] = []
    for seq in data.pages_updates:
        if not data.is_correct_sequence(seq):
            seq = data.fix_sequence(seq)
            middle.append(seq[len(seq) // 2])
    return sum(middle)


@time_duration
def run_all():
    data = parse()

    p1 = part1(data)
    p2 = part2(data)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
