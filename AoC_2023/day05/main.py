import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from utilities import time_duration

from typing import Tuple, Dict, List
from dataclasses import dataclass
import re


@dataclass
class IntervalDetails:
    destination: str
    source_start: int
    source_end: int
    destination_start: int
    delta: int

    def __init__(self, destination, destination_start, source_start, length):
        self.destination = destination
        self.source_start = source_start
        self.source_end = source_start + length-1
        self.destination_start = destination_start
        self.delta = destination_start - source_start

    def get_destination_number(self, value: int) -> int|None:
        if self.source_start <= value <= self.source_end:
            return value + self.delta
        return None


# intervals convertion for seed-to-soil ... to ... humidity-to-location
convertion_forward: Dict[str, List[IntervalDetails]] = {}
START, GOAL = "seed", "location"


@time_duration
def parse() -> Tuple[List[int], List[Tuple[int, int]]]:
    num = re.compile(r"\d+")
    conv = re.compile(r"(\w+)-to-(\w+) map:")

    with open("input.txt", mode="r", encoding="utf-8") as f:
        seeds1 = [int(n.group()) for n in num.finditer(f.readline().strip())]
        seeds2 = [(seed, seed+delta) for seed, delta in zip(seeds1[0::2], seeds1[1::2])]

        for line in f:
            line = line.strip()
            if line:
                from_to = conv.findall(line)
                if from_to:
                    _from, _to = from_to[0]
                    convertion_forward[_from] = []
                else:
                    _nums = tuple(map(int, num.findall(line)))
                    convertion_forward[_from].append(IntervalDetails(_to, *_nums))

    return seeds1, seeds2


# part 1 ----------------

def go_forward(_from: str, _goal: str, source_num: int) -> int:
    if _from == _goal:
        return source_num
    
    for interval in convertion_forward[_from]:
        new_num = interval.get_destination_number(source_num)
        if new_num is not None:
            return go_forward(interval.destination, _goal, new_num)

    return go_forward(interval.destination, _goal, source_num)


@time_duration
def part1(seeds: list) -> int:
    return min([go_forward(START, GOAL, s) for s in seeds])


# part 2 ----------------

@time_duration
def part2(seed_pair: list) -> List[int]:
    _tmp_range = seed_pair[:]
    _from, _goal = START, GOAL

    while _from != _goal:
        intervals = convertion_forward[_from]
        _to = intervals[0].destination
        _new_range = []

        while len(_tmp_range) > 0:
            first, last = _tmp_range.pop()
            for interval in intervals:
                dest_start, source_start, source_end = interval.destination_start, interval.source_start, interval.source_end
                f = max(first, source_start)
                l = min(last, source_end)
                if f < l:
                    _new_range.append([f - source_start + dest_start, l - source_start + dest_start])
                    if f > first:
                        _tmp_range.append([first, f])
                    if l < last:
                        _tmp_range.append([l, last])
                    break
            else:
                _new_range.append([first, last])

        _tmp_range, _from = _new_range, _to

    return min(_new_range)[0]


@time_duration
def all():
    seeds1, seeds2 = parse()

    p1, p2 = part1(seeds1), part2(seeds2)
    
    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    all()
