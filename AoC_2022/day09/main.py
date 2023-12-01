def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


r = {
    "input": []
}

dd = {
    "R":  (1, 0),
    "L":  (-1, 0),
    "U":  (0, -1),
    "D":  (0, 1),
}


def read_input(line: str):
    l = line.split(" ")
    r["input"].append((l[0], int(l[1])))


def far_away(p1: list, p2: list):
    return abs(p1[0] - p2[0]) > 1 or abs(p1[1] - p2[1]) > 1


def step_towards(p1: list, p2: list):
    hx, hy = p1[0], p1[1]
    tx, ty = p2[0], p2[1]
    inc_x = 0 if hx == tx else (hx - tx) // abs(hx - tx)
    inc_y = 0 if hy == ty else (hy - ty) // abs(hy - ty)
    return tx+inc_x, ty+inc_y


def calc_moves(moves: list, nknots: int = 10):
    knots = [[0, 0] for _ in range(nknots)]
    tail_places = {(0, 0)}
    for move, qtd in moves:
        mx, my = dd[move]
        for _ in range(qtd):
            knots[0][0] += mx
            knots[0][1] += my

            for k in range(nknots - 1):
                if far_away(knots[k], knots[k + 1]):
                    knots[k+1][0], knots[k+1][1] = step_towards(knots[k], knots[k + 1])

            tail_places.add(tuple(knots[-1]))

    print(f"Answer for {nknots} knots:", len(tail_places))


if __name__ == "__main__":
    parser(read_input)
    calc_moves(r["input"], 2)
    calc_moves(r["input"], 10)
