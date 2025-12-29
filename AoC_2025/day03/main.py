import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utilities import time_duration


@time_duration
def parse() -> list:
    with open("input.txt", mode="r", encoding="utf-8") as f:
        return [
            [int(batterie) for batterie in line.strip()]
            for line in f
        ]


def get_max_jolts(bank, n):
    if n == 1:
        return max(bank)
    
    leading = bank[:-(n-1)]
    leading_max = max(leading)
    leading_index = leading.index(leading_max)
    
    return leading_max * 10**(n-1) + get_max_jolts(bank[leading_index+1:], n-1)


@time_duration
def part1(l1: list, number_of_batteries: int = 2) -> int:
    return sum([get_max_jolts(bank, number_of_batteries) for bank in l1]) 


@time_duration
def part2(l1: list, number_of_batteries: int = 12) -> int:
    return sum([get_max_jolts(bank, number_of_batteries) for bank in l1]) 


@time_duration
def run_all():
    l1 = parse()

    p1 = part1(l1)
    p2 = part2(l1)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
