def parser(filename: str, method, **kwargs):
    with open(filename, mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


def read_input(line: str, p: list):
    p.append(int(line))


def solve(puzzle: list[int], times: int = 1):
    original = list(enumerate(puzzle))
    result, size = list(original), len(original)
    for _ in range(times):
        for element in original:
            result_idx = result.index(element)
            result.remove(element)
            new_idx = (result_idx + element[1]) % len(result)
            result.insert(new_idx, element)
    result = [n for _, n in result]
    zero_idx = result.index(0)
    return [result[(zero_idx + i) % size] for i in (1000, 2000, 3000)]


if __name__ == "__main__":
    pinput: list[int] = []
    parser("input.txt", read_input, p=pinput)

    r = solve(puzzle=pinput)
    print("Answer 1:", sum(r), r)

    r = solve(puzzle=[v*811589153 for v in pinput], times=10)
    print("Answer 2:", sum(r), r)
