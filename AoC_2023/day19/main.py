import sys
from collections import namedtuple

sys.path.append("../..")
from utilities import time_duration

from typing import Dict, List, Tuple
import re


Rules = List[str]
NodeRules = Dict[str, Rules]
Data = Dict[str, int]
AllData = List[Data]


@time_duration
def parse() -> Tuple[NodeRules, AllData]:
    nr: NodeRules = dict()
    ad: AllData = []
    mode_node = True

    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                if mode_node:
                    g = re.findall(r"^([a-z]+)\{(.+)\}$", line)[0]
                    nr[g[0]] = g[1].split(",")
                else:
                    ad.append({cmd.split("=")[0]: int(cmd.split("=")[1]) for cmd in line[1:-1].split(",")})
            else:
                mode_node = False

    return nr, ad


def ask(nr: NodeRules, rules: Rules, data: Data) -> int:
    for rule in rules:
        if ":" in rule:
            question, node = rule.split(":")
            if eval(question, data.copy()):
                break
        else:
            node = rule
            break

    if node == "A":
        return sum(tuple(data.values()))
    elif node == "R":
        return 0
    return ask(nr, nr[node], data)


# part 1 ----------------

@time_duration
def part1(nr: NodeRules, ad: AllData) -> int:
    return sum(ask(nr, nr["in"], data) for data in ad)


# part 2 ----------------

@time_duration
def part2(nr: NodeRules, ad: AllData) -> int:
    print(nr)
    print(ad)
    return 0


@time_duration
def run_all():
    data = parse()

    p1 = part1(*data)
    p2 = part2(*data)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
