import sys
sys.path.append("../..")
from utilities import time_duration

from typing import Tuple, List
import re


NumSeq = List[int]


@time_duration
def parse() -> List[NumSeq]:
    num = re.compile(r"-?\d+")
    nums_list = []
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            nums_list.append([int(n.group()) for n in num.finditer(line)])
    return nums_list


def _get_diffs(nums: NumSeq) -> NumSeq:
    return [nums[i+1] - nums[i] for i in range(len(nums)-1)]


def _get_diffs_piramid(nums: NumSeq) -> List[NumSeq]:
    piramid, curr_diff = [nums[:]], nums
    while any(curr_diff) > 0:
        curr_diff = _get_diffs(curr_diff)
        piramid.append(curr_diff)
    return piramid


# part 1 ----------------

def predict_top_right_value(nums: NumSeq) -> int:
    return sum([row[-1] for row in _get_diffs_piramid(nums)])


@time_duration
def part1(nums_list: List[NumSeq]) -> int:
    return sum([predict_top_right_value(nums) for nums in nums_list])


# part 2 ----------------

def predict_top_left_value(nums: NumSeq) -> int:
    res = 0
    for row in _get_diffs_piramid(nums)[::-1]:
        res = row[0] - res
    return res


@time_duration
def part2(nums_list: List[NumSeq]) -> int:
    return sum([predict_top_left_value(nums) for nums in nums_list])


@time_duration
def all():
    nums_list = parse()

    p1 = part1(nums_list)
    p2 = part2(nums_list)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    all()
