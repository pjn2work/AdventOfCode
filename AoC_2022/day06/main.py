def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


def find_ne_chars(line: str, many: int = 4) -> int:
    end = len(line) - many
    for i in range(end):
        pattern = line[i:i+many]
        if len(set(pattern)) == many:
            return i
    raise LookupError(f"No pattern found for {many} chars")


def show_findings(line, many):
    x = find_ne_chars(line, many) + many
    print(f"Answer for {many} chars pattern:", x, line[x-many:x])


def find_pattern(line: str):
    show_findings(line, 4)
    show_findings(line, 14)


if __name__ == "__main__":
    parser(find_pattern)
