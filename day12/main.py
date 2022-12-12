from dataclasses import dataclass, field


def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


@dataclass(unsafe_hash=True)
class Point2D:
    x: int
    y: int


@dataclass
class Puzzle:
    input: list[list[int]]
    starts: list[Point2D]
    end: Point2D
    rows: int = field(default=0)
    cols: int = field(default=0)


moves = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1)
}


def height(x: int, c: str, p: Puzzle) -> int:
    if c in ["S", "a"]:
        p.starts.append(Point2D(x=x, y=p.rows))
        return 0
    if c == "E":
        p.end = Point2D(x=x, y=p.rows)
        return ord("z")-ord("a")
    return ord(c)-ord("a")


def read_input(line: str, p: Puzzle):
    p.input.append([height(x, c, p) for x, c in enumerate(line)])
    p.cols = len(line)
    p.rows += 1


def shortest_path(p: Puzzle, start: Point2D):
    visited = set([start])
    to_visit = [(start, 0, "")]  # point_where_I_am_atm, dist_accumulated, route_taken_choices

    while to_visit:
        curr_pos, dist, route = to_visit.pop(0)
        if curr_pos == p.end:
            return dist, route

        for move, (inc_y, inc_x) in moves.items():
            new_pos = Point2D(y=curr_pos.y + inc_y, x=curr_pos.x + inc_x)
            if 0 <= new_pos.y < p.rows and 0 <= new_pos.x < p.cols and new_pos not in visited:
                my_h, new_h = p.input[curr_pos.y][curr_pos.x], p.input[new_pos.y][new_pos.x]
                if new_h <= my_h + 1:
                    to_visit.append((new_pos, dist+1, route+move))
                    visited.add(new_pos)

    return float("inf"), ""


if __name__ == "__main__":
    puzzle = Puzzle(input=[], starts=[], end=None)
    parser(read_input, p=puzzle)

    answer, route = shortest_path(puzzle, puzzle.starts[0])
    print("Answer 1:", answer, "| Route", route)

    answer, route = min([shortest_path(puzzle, start=start) for start in puzzle.starts])
    print("Answer 2:", answer, "| Route", route)
