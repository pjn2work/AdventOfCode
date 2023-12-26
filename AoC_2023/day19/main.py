import sys
from collections import namedtuple

sys.path.append("../..")
from utilities import time_duration, prod

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

RuleDetail = namedtuple("RuleDetail", "var op value next_node")
Limits = namedtuple("Limits", "low high")

def parse_node_rules(nr: NodeRules) -> Dict[str, List[RuleDetail]]:
    _rules = dict()
    for node, rules in nr.items():
        _rules[node] = []
        for rule in rules:
            if ":" in rule:
                question, next_node = rule.split(":")
                _rules[node].append(RuleDetail(var=question[0], op=question[1], value=int(question[2:]), next_node=next_node))
            else:
                _rules[node].append(rule)
    # {"px": [('a', '<', 2006, 'qkq'), ('m', '>', 2090, 'A'), 'rfg'], ...}
    return _rules


@time_duration
def part2(nr: NodeRules) -> int:
    res = 0
    flows = parse_node_rules(nr)
    queue = [("in", 0, {var: Limits(1, 4000) for var in "xmas"})]

    while len(queue) > 0:
        curr_node, idx, bounds = queue.pop()

        if curr_node == "A":
            res += prod(bounds[var][1] - bounds[var].low + 1 for var in "xmas")
            continue

        if curr_node == "R":
            continue

        step = flows[curr_node][idx]

        if isinstance(step, str):
            queue.append((step, 0, bounds))
        elif step.op == "<":
            true = bounds.copy()
            false = bounds

            true[step.var] = Limits(true[step.var].low, step.value - 1)
            false[step.var] = Limits(step.value, false[step.var].high)

            queue.append((step.next_node, 0, true))
            if idx+1 < len(flows[curr_node]):
                queue.append((curr_node, idx + 1, false))
        elif step.op == ">":
            true = bounds.copy()
            false = bounds

            true[step.var] = Limits(step.value + 1, true[step.var][1])
            false[step.var] = Limits(false[step.var][0], step.value)

            queue.append((step.next_node, 0, true))
            if idx+1 < len(flows[curr_node]):
                queue.append((curr_node, idx + 1, false))

    return res


@time_duration
def run_all():
    nr, ad = parse()

    p1 = part1(nr, ad)
    p2 = part2(nr)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
