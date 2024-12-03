import re

from utilities import time_duration


Data = str
mul_pattern = r"mul\((\d{1,3}),(\d{1,3})\)"


@time_duration
def parse() -> Data:
    data: Data = ""
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            v = line.strip()
            data += v
    return data


@time_duration
def part1(data: Data) -> int:
    matches = re.findall(mul_pattern, data)

    result = 0
    for match in matches:
        x = int(match[0])
        y = int(match[1])
        result += x * y

    return result


@time_duration
def part2(data: Data) -> int:
    # Track enabled state
    is_enabled = True
    result = 0

    # Split text into tokens to process sequentially
    pattern = r"mul\(\d+,\d+\)|do\(\)|don't\(\)"
    tokens = re.findall(pattern, data)

    for token in tokens:
        if token == "do()":
            is_enabled = True
        elif token == "don't()":
            is_enabled = False
        elif is_enabled and "mul" in token:
            match = re.match(mul_pattern, token)
            if match:
                x, y = map(int, match.groups())
                result += x * y

    return result


@time_duration
def run_all():
    data = parse()

    p1 = part1(data)
    p2 = part2(data)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
