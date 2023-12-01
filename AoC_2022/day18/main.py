def parser(filename: str, method, **kwargs):
    with open(filename, mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


def read_input(line: str, d: set):
    d.add(tuple(map(int, line.split(","))))


def free_neighbors(x, y, z) -> tuple[tuple[int, int, int], int]:
    for dim in range(3):
        for inc in (-1, 1):
            p = [x, y, z]
            p[dim] += inc
            if (p := tuple(p)) not in droplets:
                yield p, dim


def propagate(point: tuple[int, int, int], edge_min: list[int, int, int], edge_max: list[int, int, int], outside: set, air_pockets: set) -> bool:
    already_connected: set[tuple[int, int, int]] = set()
    handle_points: list[tuple[int, int, int]] = [point]
    while handle_points:
        curr_point = handle_points.pop()
        for free_point, dim in free_neighbors(*curr_point):
            if free_point[dim] < edge_min[dim] or edge_max[dim] < free_point[dim]:
                outside.update(already_connected)
                return True
            if free_point not in already_connected:
                already_connected.add(free_point)
                handle_points.append(free_point)

    air_pockets.update(already_connected)
    return False


def solve():
    edge_min = [min(drop[dim] for drop in droplets) for dim in range(3)]
    edge_max = [max(drop[dim] for drop in droplets) for dim in range(3)]

    answer1, answer2 = 0, 0
    air_pockets, outside = set(), set()
    for drop in droplets:
        for point, _ in free_neighbors(*drop):
            answer1 += 1
            if point not in air_pockets and (point in outside or propagate(point, edge_min, edge_max, outside, air_pockets)):
                answer2 += 1

    print(f"{len(droplets)=} {edge_min=}, {edge_max=}\n")
    print("Answer 1:", answer1)
    print("Answer 2:", answer2)


if __name__ == "__main__":
    droplets = set()
    parser("input.txt", read_input, d=droplets)
    solve()
