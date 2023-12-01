import re


def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


def read_input(line: str, p: dict[str, str]):
    data = re.search(r"^([a-z]+): (.+)", line)
    monkey = data.group(1)
    try:
        p[monkey] = float(data.group(2))
    except:
        p[monkey] = data.group(2)


def calculate(name: str) -> float:
    value = puzzle[name]
    if isinstance(value, float):
        return value

    left, right, parts = None, None, value.split(" ")
    try:
        left = calculate(parts[0])
        puzzle[name] = puzzle[name].replace(parts[0], str(left))
    except:
        pass
    try:
        right = calculate(parts[2])
        puzzle[name] = puzzle[name].replace(parts[2], str(right))
    except:
        pass

    if left is None and right is None:
        raise ValueError(f"Can't calculate {parts}")

    puzzle[name] = eval(f"{left} {parts[1]} {right}")
    return puzzle[name]


def answer1():
    parser(read_input, p=puzzle)
    print("Answer 1:", calculate("root"))


def extract_var_op_value(s: str) -> tuple[str, str, float, bool]:
    x = s.split(" ")
    try:
        var, op, value2, inv = x[0], x[1], float(x[2]), False
    except:
        var, op, value2, inv = x[2], x[1], float(x[0]), True
    return var, op, value2, inv


def calculate_inverse(var1, value1) -> float:
    inv_op = {"+": "-", "-": "+", "*": "/", "/": "*"}
    if var1 == "humn":
        return value1
    var2, op, value2, inv = extract_var_op_value(puzzle[var1])

    if inv and op in ["-", "/"]:
        value1, value2, op = value2, value1, inv_op[op]

    return calculate_inverse(var2, eval(f"{value1} {inv_op[op]} {value2}"))


def answer2():
    parser(read_input, p=puzzle)
    puzzle["humn"] = "NOT_DEFINED"

    try:
        calculate("root")
    except:
        pass

    var1, _, value1, _ = extract_var_op_value(puzzle["root"])
    print("Answer 2:", calculate_inverse(var1, value1))


if __name__ == "__main__":
    puzzle: dict[str, float] = dict()
    answer1()
    answer2()
