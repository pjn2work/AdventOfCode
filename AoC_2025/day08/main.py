import sys
import os
import math
from itertools import combinations

# Add project root to sys.path
CWD = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(CWD, "../..")))

from utilities import time_duration



Point = tuple[int, int, int]
Connection = tuple[Point, Point]
Circuit = set[Point]


@time_duration
def parse() -> list[Point]:
    with open(os.path.join(CWD, "input.txt"), mode="r", encoding="utf-8") as f:
        return [tuple(map(int, line.strip().split(","))) for line in f]


def calc_dist_between_boxes(l1: list[Point]) -> dict[Connection, float]:
    result = {(min(box1, box2), max(box1, box2)): math.dist(box1, box2) for box1, box2 in combinations(l1, 2)}
    return dict(sorted(result.items(), key=lambda item: item[1]))


def get_circuit_for_box(circuits: list[Circuit], box: Point) -> Circuit | None:
    for circuit in circuits:
        if box in circuit:
            return circuit
    return None



@time_duration
def part1(l1: list, top_connections: int = 1000, top_circuits: int = 3) -> int:
    circuits: list[Circuit] = []
    ordered_connections = calc_dist_between_boxes(l1)
    
    for (box1, box2), dist in ordered_connections.items():
        top_connections -= 1
        if top_connections < 0:
            break

        for circuit in circuits:
            if box1 in circuit or box2 in circuit:
                other_box = box1 if box2 in circuit else box2
                other_circuit = get_circuit_for_box(circuits, other_box)
                if other_circuit and other_circuit != circuit:
                    circuits.remove(other_circuit)
                    circuit.update(other_circuit)
                else:
                    circuit.add(other_box)
                break
        else:
            circuits.append({box1, box2})
    
    # sort circuits by size
    circuits = sorted(circuits, key=len, reverse=True)

    return math.prod(len(circuit) for circuit in circuits[:top_circuits])


@time_duration
def part2(l1: list) -> int:
    circuits: list[Circuit] = []
    ordered_connections = calc_dist_between_boxes(l1)
    last_added_connection = None
    
    for (box1, box2), dist in ordered_connections.items():
        for circuit in circuits:
            if box1 in circuit or box2 in circuit:
                other_box = box1 if box2 in circuit else box2
                other_circuit = get_circuit_for_box(circuits, other_box)
                if other_circuit and other_circuit != circuit:
                    circuits.remove(other_circuit)
                    circuit.update(other_circuit)
                else:
                    if other_box not in circuit:
                        last_added_connection = (box1, box2)
                        circuit.add(other_box)
                break
        else:
            circuits.append({box1, box2})
   
    return last_added_connection[0][0] * last_added_connection[1][0]


@time_duration
def run_all():
    l1 = parse()

    p1 = part1(l1)
    p2 = part2(l1)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
