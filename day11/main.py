import math
import re
import copy


def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


r = {
    "monkey": dict(),
    "play_order": [],
    "curr_monkey": None
}


class Monkey:
    def __init__(self, n: int):
        self.n = n
        self.inspections = 0

        self.items_worry_level = []
        self.operation = ""
        self.divisible_by = 0
        self.test = {True: None, False: None}

    def add_item_wl(self, wl: int, cd: int):
        if cd is None:
            self.items_worry_level.append(wl)
        else:
            self.items_worry_level.append(wl % cd)

    def calc_worry_level(self, wl: int, bored: int) -> int:
        return eval(self.operation.replace("old", str(wl))) // bored

    def play(self, monkeys: dict, bored: int, cd: int):
        while len(self.items_worry_level) > 0:
            self.inspections += 1
            item = self.items_worry_level.pop(0)

            wl = self.calc_worry_level(item, bored=bored)
            t = wl % self.divisible_by == 0
            n = self.test[t]

            monkeys[n].add_item_wl(wl, cd)

    def __repr__(self):
        return f"Monkey {self.n} | {self.inspections=} | {self.divisible_by=} | {self.operation=} | {self.test} | {self.items_worry_level}"


def read_input(line: str):
    if line.startswith("Monkey "):
        res = re.search("Monkey (\\d+).$", line)
        n = int(res.group(1))
        r["monkey"][n] = r["curr_monkey"] = Monkey(n)
        r["play_order"].append(n)
    elif line.startswith("Starting items: "):
        items = line[16:].split(",")
        r["curr_monkey"].items_worry_level = [int(i) for i in items]
    elif line.startswith("Operation: new = old "):
        r["curr_monkey"].operation = line[17:]
    elif line.startswith("Test: divisible by "):
        r["curr_monkey"].divisible_by = int(line[19:])
    elif line.startswith("If "):
        res = re.search("If ([a-z]+): throw to monkey (\\d+)$", line)
        b = res.group(1) == "true"
        n = int(res.group(2))
        r["curr_monkey"].test[b] = n
    elif line == "":
        r["curr_monkey"] = None
    else:
        raise AssertionError(f"Instruction not expected {line}")


def answer(id: int, monkeys: dict, play_order: list, bored: int, rounds: int, cd: int):
    for _ in range(rounds):
        for n in play_order:
            monkeys[n].play(monkeys=monkeys, bored=bored, cd=cd)

    print(f"\n----- Answer {id} after {rounds=}", "-"*80)
    for monkey in monkeys.values():
        print(monkey)

    inspections = [m.inspections for m in monkeys.values()]
    maxi = sorted(inspections, reverse=True)[:2]
    print(f"**** Answer {id}:", math.prod(maxi), "From:", maxi, "*****")


if __name__ == "__main__":
    parser(read_input)

    print(f"----- Initial setup", "-"*80)
    for m in r["play_order"]:
        print(r["monkey"][m])

    answer(id=1, monkeys=copy.deepcopy(r["monkey"]), play_order=r["play_order"], bored=3, rounds=20, cd=None)

    common_divisor = math.prod(m.divisible_by for m in r["monkey"].values())
    answer(id=2, monkeys=copy.deepcopy(r["monkey"]), play_order=r["play_order"], bored=1, rounds=10000, cd=common_divisor)
