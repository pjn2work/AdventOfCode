def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


def gen_results() -> dict:
    return {
        "blank": 0,
        "err": 0,
        "good": 0,
        "stacks": dict()
    }


def pile_line_stack(line: str, r: dict):
    l = len(line)
    for i in range(1, 99, 4):
        if i > l:
            return
        stack = str((i-1)//4 + 1)
        v = line[i].strip()
        if v:
            if stack not in r["stacks"]:
                r["stacks"][stack] = [v]
            else:
                r["stacks"][stack] = [v] + r["stacks"][stack]


def move_crane_9000(line: str, r: dict):
    line = line.split(" ")
    q, f, t = line[1], line[3], line[5]
    unpile_stack_9000(int(q), f, t, r)


def unpile_stack_9000(q, f, t, r: dict):
    for _ in range(q):
        r["stacks"][t].append(r["stacks"][f].pop())


def move_crane_9001(line: str, r: dict):
    line = line.split(" ")
    q, f, t = line[1], line[3], line[5]
    unpile_stack_9001(int(q), f, t, r)


def unpile_stack_9001(q, f, t, r: dict):
    crates = r["stacks"][f][-q:]
    r["stacks"][t] += crates
    r["stacks"][f] = r["stacks"][f][:-q]


def move_crane(line: str, crane=None, r: dict = {}):
    if not line:
        r["blank"] += 1
        return
    try:
        if line.startswith("["):
            pile_line_stack(line, r)
        elif line.startswith("move"):
            crane(line, r)
        else:
            return
        r["good"] += 1

    except AssertionError as ex:
        r["err"] += 1
        print(ex)


def puzzle(crane=move_crane_9001):
    res = gen_results()
    parser(move_crane, crane=crane, r=res)

    answer = ""
    print("\n\nFinal layout")
    for stack in sorted(res["stacks"]):
        values = res["stacks"][stack]
        answer += values[-1]
        print(stack, values)
    print(res, f"\nAnswer {crane.__name__} = {answer}")


if __name__ == "__main__":
    puzzle(move_crane_9000)
    puzzle(move_crane_9001)
