import timeit


def parser(method):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip())


r = {
    "blank": 0,
    "err": 0,
    "good": 0,
    "elf": {
        "curr_id": 0,
        "curr_sum": 0,
        "max": 0,
        "max_id": 0
    },
    "max_list": [0 for _ in range(3)]
}


def calories(line):
    if not line:
        r["blank"] += 1
        if r["elf"]["curr_sum"] > r["elf"]["max"]:
            r["elf"]["max"] = r["elf"]["curr_sum"]
            r["elf"]["max_id"] = r["elf"]["curr_id"]

        for i in range(len(r["max_list"])):
            if r["elf"]["curr_sum"] > r["max_list"][i]:
                r["max_list"][i] = r["elf"]["curr_sum"]
                break
        r["elf"]["curr_id"] += 1
        r["elf"]["curr_sum"] = 0
        return

    try:
        v = int(line)
        r["good"] += 1
        r["elf"]["curr_sum"] += v
    except:
        r["err"] += 1


if __name__ == "__main__":
    t = timeit.Timer()
    parser(calories)
    print(t.timeit(), r)
    print("Answer 1 =", r["elf"]["max"])
    print("Answer 2 =", sum(r["max_list"]))
