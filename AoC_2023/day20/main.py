import sys
sys.path.append("../..")
from utilities import time_duration

from collections import namedtuple
from typing import Dict, List, Tuple
import re


Node = namedtuple("Node", "type nodes state")
Data = Dict[str, Node]


@time_duration
def parse() -> Data:
    res: Data = dict()
    _conjunctions = set()

    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            name, nodes = re.findall(r"^(.+) -> (.+)$", line.strip())[0]

            node_type = name[0]
            nodes = [node.group(0) for node in re.finditer("[a-z]+", nodes)]
            state = [dict()] if node_type == "&" else [False]

            res[name[1:]] = Node(node_type, nodes, state)

            if node_type == "&":
                _conjunctions.add(name[1:])

    # set all conjunctions inputs as Low
    for conjunction in _conjunctions:
        for node_name, node in res.items():
            if conjunction in node.nodes:
                res[conjunction].state[0][node_name] = False

    return res


def broadcast(data: Data, exec_queue: List[Tuple[str, str, bool]], lows: int = 0, highs: int = 0) -> Tuple[int, int]:
    while exec_queue:
        name_from, name_dst, input_state = exec_queue.pop(0)
        node = data.get(name_dst)

        if input_state:
            highs += 1
        else:
            lows += 1

        if node:
            if node.type == "&":                # Conjunction
                node.state[0][name_from] = input_state
                output_state = not all(node.state[0].values())
            elif node.type == "%":              # Flip-flop
                if input_state:
                    continue
                output_state = node.state[0] = not node.state[0]
            else:                               # Broadcaster
                output_state = input_state

            for name_next in node.nodes:
                exec_queue.append((name_dst, name_next, output_state))

    return lows, highs


# part 1 ----------------

@time_duration
def part1(data: Data) -> int:
    lows = highs = 0
    for _ in range(1000):
        lows, highs = broadcast(data, [("button", "roadcaster", False)], lows, highs)
    return lows * highs


# part 2 ----------------

@time_duration
def part2(data: Data) -> int:
    return 0


@time_duration
def run_all():
    data = parse()

    p1 = part1(data)
    p2 = part2(data)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
