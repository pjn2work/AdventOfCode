import os, sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)
from utilities import time_duration

from typing import Tuple, List, Dict
from collections import namedtuple
from itertools import cycle
import math
import re


Node = namedtuple("Node", ["next", "cost"])
routes: Dict[str, Dict[str, Node]] = {}
neighbours: Dict[str, Tuple[str, str]] = {}


@time_duration
def parse() -> List[int]:
    node = re.compile(r"\w{3}")
    with open("input.txt", mode="r", encoding="utf-8") as f:
        directions = [int(d) for d in f.readline().strip().replace("L", "0").replace("R", "1")]
        f.readline()

        for line in f:
            grp = node.findall(line.strip())
            routes[grp[0]] = {
                grp[1]: Node(grp[1], 1),
                grp[2]: Node(grp[2], 1)
            }
            neighbours[grp[0]] = (grp[1], grp[2])

    return directions


part1_goal = lambda node: node == "ZZZ"
part2_goal = lambda node: node.endswith("Z")


def steps_to_goal(directions: List[int], node: str, goal_function) -> int:
    _steps = 0
    for d in cycle(directions):
        _steps += 1
        node = neighbours[node][d]
        if goal_function(node):
            break
    return _steps


# part 1 ----------------

@time_duration
def part1(directions: List[int]) -> int:
    return steps_to_goal(directions, "AAA", part1_goal)


# part 2 ----------------

@time_duration
def part2(directions: List[int]) -> int:
    _starts = [node for node in neighbours if node.endswith("A")]
    _steps = [steps_to_goal(directions, node, part2_goal) for node in _starts]

    print([(n, s) for n, s in zip(_starts, _steps)])

    # for all ghosts be in a xxZ node
    return math.lcm(*_steps)


@time_duration
def all():
    directions = parse()

    p1 = part1(directions)
    p2 = part2(directions)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    all()
