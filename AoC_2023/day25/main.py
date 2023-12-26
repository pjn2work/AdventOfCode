import sys
sys.path.append("../..")
from utilities import time_duration

from typing import List, Tuple
import networkx as nx


Data = List[Tuple[str, List[str]]]


@time_duration
def parse() -> Data:
    data = []
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            nl, nr = line.strip().split(": ")
            data.append((nl, nr.split(" ")))
    return data


# part 1 ----------------

@time_duration
def part1(data: Data) -> int:
    graph = nx.Graph()

    for node, neighbors in data:
        for neighbor in neighbors:
            graph.add_edge(node, neighbor)

    links_cut, groups = nx.stoer_wagner(graph)
    assert links_cut == 3

    return len(groups[0]) * len(groups[1])


@time_duration
def run_all():
    data = parse()

    p1 = part1(data)
    print(f"Result for {p1 = }")


if __name__ == "__main__":
    run_all()
