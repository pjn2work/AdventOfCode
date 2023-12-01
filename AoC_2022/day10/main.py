def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


r = {
    "cycle": 0,
    "x": 1,
    "wanted_cycles": (20, 60, 100, 140, 180, 220),
    "scores1": [],
    "screen2": [["  "] * 40 for _ in range(6)]
}


# Answer 1
def calc_score():
    r["cycle"] += 1
    if r["cycle"] in r["wanted_cycles"]:
        r["scores1"].append(r["cycle"] * r["x"])


# Answer 2
def build_letters():
    cursor = r["cycle"] -1
    row, col = cursor // 40, cursor % 40
    if abs(r["x"] - col) <= 1:
        r["screen2"][row][col] = "O "


def solve(line: str):
    if line == "noop":
        calc_score()
        build_letters()
    elif line.startswith("addx"):
        calc_score()
        build_letters()

        calc_score()
        build_letters()

        l = line.split(" ")
        r["x"] += int(l[1])
    else:
        raise AssertionError(f"Instruction not expected {line}")


if __name__ == "__main__":
    parser(solve)

    print("Answer 1:", sum(r["scores1"]), r["scores1"])

    print("Answer 2:")
    for row in r["screen2"]:
        print("".join(row))
