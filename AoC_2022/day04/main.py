def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


def extract_sections(line):
    s1, s2 = line.split(",")
    s1_a, s1_z = s1.split("-")
    s2_a, s2_z = s2.split("-")
    return int(s1_a), int(s1_z), int(s2_a), int(s2_z)


def check_fully_contains(s1_a, s1_z, s2_a, s2_z) -> bool:
    return (s1_a <= s2_a and s1_z >= s2_z) or (s2_a <= s1_a and s2_z >= s1_z)


def check_overlaps(s1_a, s1_z, s2_a, s2_z) -> bool:
    return (s1_a <= s2_a <= s1_z) or (s1_a <= s2_z <= s1_z)


r = {
    "blank": 0,
    "err": 0,
    "good": 0,
    "p1_score": 0,
    "p2_score": 0
}


def sections_2elfs(line: str):
    if not line:
        r["blank"] += 1
        return
    try:
        r["good"] += 1

        sections = extract_sections(line)
        if check_fully_contains(*sections):
            r["p1_score"] += 1
            r["p2_score"] += 1
        elif check_overlaps(*sections):
            r["p2_score"] += 1

    except AssertionError as ex:
        r["err"] += 1
        print(ex)


if __name__ == "__main__":
    parser(sections_2elfs)
    print(r, f"\nAnswer 1 = {r['p1_score']}\nAnswer 2 = {r['p2_score']}")
