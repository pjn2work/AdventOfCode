import sys
sys.path.append("../..")
from utilities import time_duration

from collections import namedtuple
from typing import List, Tuple, Dict, Set


Point = namedtuple("Point", "y x")
Data = List[str]
MOVES = {
    "^": [Point(-1, 0)],
    "<": [Point(0, -1)],
    "v": [Point(1, 0)],
    ">": [Point(0, 1)],
    ".": [Point(-1, 0), Point(0, -1), Point(1, 0), Point(0, 1)]
}
GRAPH = Dict[Point, Dict[Point, int]]


@time_duration
def parse() -> Tuple[Data, Point, Point]:
    data = []
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            data.append(line.strip())
    return data, Point(0, data[0].index(".")), Point(len(data)-1, data[-1].index("."))


# part 1 ----------------

@time_duration
def part1(data: Data, curr_pos: Point, goal: Point) -> int:
    ly, lx = len(data), len(data[0])
    res = 0
    queue_next = [(curr_pos, {curr_pos})]

    while queue_next:
        curr_pos, visited = queue_next.pop()

        if curr_pos == goal:
            res = max(res, len(visited))

        for inc in MOVES[data[curr_pos.y][curr_pos.x]]:
            cp = Point(curr_pos.y + inc.y, curr_pos.x + inc.x)
            if 0 <= cp.y < ly and 0 <= cp.x < lx and data[cp.y][cp.x] != "#" and cp not in visited:
                queue_next.append((cp, visited | {cp}))

    return res-1


# part 2 ----------------

def convert_map_to_graph(data: Data) -> GRAPH:
    ly, lx = len(data), len(data[0])
    graph: GRAPH = dict()

    for y in range(ly):
        for x in range(lx):
            _from = Point(y, x)
            if data[_from.y][_from.x] != "#":
                graph[_from] = dict()

                for inc in MOVES["."]:
                    _to = Point(_from.y + inc.y, _from.x + inc.x)
                    if 0 <= _to.y < ly and 0 <= _to.x < lx and data[_to.y][_to.x] != "#":
                        graph[_from][_to] = 1
                        if _to not in graph:
                            graph[_to] = dict()
                        graph[_to][_from] = 1
    return graph


def get_intersections_distances(graph: GRAPH) -> GRAPH:
    for point in set(graph.keys()):
        neighbours = graph[point]
        if len(neighbours) == 2:
            p1, p2 = neighbours
            distance = neighbours[p1] + neighbours[p2]

            # save distance between both ends
            graph[p1][p2] = distance
            graph[p2][p1] = distance

            # delete intermediate "point" and distance to him
            del graph[point]
            del graph[p1][point]
            del graph[p2][point]

    return graph


def find_all_paths_length(graph: GRAPH, curr_point: Point, goal: Point, visited: Set, curr_length: int, all_lengths: List[int]):
    if curr_point == goal:
        all_lengths.append(curr_length)
        return

    for edge_point in graph[curr_point]:
        if edge_point not in visited:
            new_length = curr_length + graph[curr_point][edge_point]
            find_all_paths_length(graph, edge_point, goal, visited | {edge_point}, new_length, all_lengths)


@time_duration
def part2(data: Data, start: Point, goal: Point) -> int:
    graph = get_intersections_distances(convert_map_to_graph(data))

    all_lengths = []
    find_all_paths_length(graph, start, goal, set(), 0, all_lengths)
    return max(all_lengths)


@time_duration
def run_all():
    data, start, goal = parse()

    p1 = part1(data, start, goal)
    p2 = part2(data, start, goal)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
