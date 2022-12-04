def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


def get_priority(l: str) -> int:
    m, m1, m2 = ord(l), ord("A"), ord("a")
    if m >= m2:
        return m-m2+1
    return m-m1+27


def split_rucksacks(line: str) -> (str, str):
    h = len(line) // 2
    return line[:h], line[h:]


def find_common_letter(s1, s2) -> str:
    for s in s1:
        if s in s2:
            return s
    raise ValueError(f"No common letter between '{s1}' and '{s2}'")


def find_common_letter_in3(s1, s2, s3) -> str:
    for s in s1:
        if s in s2 and s in s3:
            return s
    raise ValueError(f"No common letter between '{s1}' and '{s2}' and '{s3}'")


r = {
    "blank": 0,
    "err": 0,
    "good": 0,
    "p1_score": 0,
    "p2": {
        "lines": {
            1: "",
            2: ""
        },
        "score": 0
    }
}


def rucksack(line: str):
    if not line:
        r["blank"] += 1
        return
    try:
        r["good"] += 1

        # puzzle 1
        r1, r2 = split_rucksacks(line)
        l = find_common_letter(r1, r2)
        r["p1_score"] += get_priority(l)

        # puzzle 2
        n = r["good"] % 3
        if n == 0:
            cl = find_common_letter_in3(r["p2"]["lines"][1], r["p2"]["lines"][2], line)
            r["p2"]["score"] += get_priority(cl)
        else:
            r["p2"]["lines"][n] = line
    except AssertionError as ex:
        r["err"] += 1
        print(ex)


if __name__ == "__main__":
    parser(rucksack)
    print(r, f"\nAnswer 1 = {r['p1_score']}\nAnswer 2 = {r['p2']['score']}")
