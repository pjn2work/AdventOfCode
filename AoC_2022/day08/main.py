import numpy as np


def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


r = {
    "input": []
}


def read_matrix(line: str):
    r["input"].append([int(v) for v in line])


def create_matrix() -> np.ndarray:
    parser(read_matrix)
    return np.array(r["input"])


def answer1(grid: np.ndarray):
    ly, lx = len(grid), len(grid[0])
    res = np.zeros((ly, lx), dtype=int)

    for y in range(ly):
        for x in range(lx):
            h = grid[y, x]
            if x == 0 or y == 0 or \
                x == lx-1 or y == ly-1 or \
                np.amax(grid[y, :x]) < h or np.amax(grid[y, x + 1:]) < h or \
                np.amax(grid[:y, x]) < h or np.amax(grid[y + 1:, x]) < h:
                    res[y, x] = 1

    print("Answer1:", np.sum(res), "\n", res)


def answer2(grid: np.ndarray):
    ly, lx = len(grid), len(grid[0])
    res = np.zeros((ly, lx), dtype=int)              # score grid
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up

    for y in range(ly):
        for x in range(lx):
            h = grid[y, x]
            score = 1

            for dy, dx in directions:
                py, px, distance = y+dy, x+dx, 0
                while (0 <= py < ly) and (0 <= px < lx):
                    distance += 1
                    if grid[py, px] >= h:
                        break
                    py, px = py+dy, px+dx

                score *= distance
                if score == 0:
                    break

            res[y, x] = score

    print("Answer2:", np.amax(res), np.unravel_index(res.argmax(), res.shape), "\n",  res)


if __name__ == "__main__":
    g = create_matrix()
    answer1(g)
    answer2(g)
