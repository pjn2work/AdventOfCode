import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utilities import time_duration


@time_duration
def parse() -> list:
    with open("input.txt", mode="r", encoding="utf-8") as f:
        return [line.strip() for line in f]


@time_duration
def part1(l1: list, dial_pos: int, dial_max_pos: int) -> int:
    zero_counter = 0
    for rotation in l1:
        move, clicks = rotation[0], int(rotation[1:]) % dial_max_pos
        if move == "L":
            clicks = clicks * -1
        
        dial_pos = (dial_pos + clicks) % dial_max_pos
        
        if dial_pos == 0:
            zero_counter += 1
        
        #print(f"{rotation = } {Data.DIAL_POS = } {times_0 = }")
    
    return zero_counter


@time_duration
def part2(l1: list, dial_pos: int, dial_max_pos: int) -> int:
    zero_counter = 0
    for rotation in l1:
        move, o_clicks = rotation[0], int(rotation[1:])        
        clicks = o_clicks % dial_max_pos
        if move == "L":
            clicks = clicks * -1

        if o_clicks >= dial_max_pos:
            zero_counter += o_clicks // dial_max_pos
        
        old_dial_pos = dial_pos
        dial_pos = dial_pos + clicks
        
        if dial_pos <= 0 or dial_pos >= dial_max_pos:
            dial_pos = dial_pos % dial_max_pos
            if old_dial_pos != 0:
                zero_counter += 1
        
        #print(f"{rotation = } {dial_pos = } {zero_counter = }")
    
    return zero_counter


@time_duration
def run_all():
    l1 = parse()

    p1 = part1(l1, 50, 100)
    p2 = part2(l1, 50, 100)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
