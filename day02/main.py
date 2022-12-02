def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


# Score = Rock 1, Paper 2, Scissors 3
ABC = {"A": 1, "B": 2, "C": 3}
XYZ = {"X": 1, "Y": 2, "Z": 3}

LOSE = {"A": "Z", "B": "X", "C": "Y"}
DRAW = {"A": "X", "B": "Y", "C": "Z"}
WIN =  {"A": "Y", "B": "Z", "C": "X"}


def get_move(a: str, x: str):
    if x == "X":
        return LOSE[a]
    if x == "Y":
        return DRAW[a]
    return WIN[a]


def score(line: str, p2: bool):
    a, x = line.split(" ")

    if a not in ABC:
        raise AssertionError(f"{a} not a ABC")
    if x not in XYZ:
        raise AssertionError(f"{x} not a XYZ")

    if p2:
        x = get_move(a, x)
    sa, sx = ABC[a], XYZ[x]

    # Lose 0, Draw 3, Win 6
    if sa == sx:
        return sa+3, sx+3
    if abs(sa-sx) == 1:
        if sa < sx:
            return sa, sx+6
        return sa+6, sx
    if sa == 1:
        return sa+6, sx
    return sa, sx+6


r = {
    "blank": 0,
    "err": 0,
    "good": 0,
    "score1": {
        "ABC": 0,
        "XYZ": 0
    },
    "score2": {
        "ABC": 0,
        "XYZ": 0
    }
}


def rock_paper_scissors(line: str):
    if not line:
        r["blank"] += 1
        return
    try:
        sa1, sx1 = score(line, False)
        sa2, sx2 = score(line, True)
        r["good"] += 1
        r["score1"]["ABC"] += sa1
        r["score1"]["XYZ"] += sx1
        r["score2"]["ABC"] += sa2
        r["score2"]["XYZ"] += sx2
    except AssertionError:
        r["err"] += 1


if __name__ == "__main__":
    parser(rock_paper_scissors)
    print(r, f"\nAnswer 1 = {r['score1']['XYZ']}\nAnswer 2 = {r['score2']['XYZ']}")
