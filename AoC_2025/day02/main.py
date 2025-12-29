import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utilities import time_duration


@time_duration
def parse() -> list:
    with open("input.txt", mode="r", encoding="utf-8") as f:
        return [
            ids.split("-")
            for line in f
            for ids in line.strip().split(",")
        ]


@time_duration
def part1(l1: list) -> int:
    invalid_ids = []
    for (id1, id2) in l1:
        id1, id2 = int(id1), int(id2)
        for id_int in range(id1, id2 + 1):
            id_str = str(id_int)
            if len(id_str) % 2 == 0:
                idl, idr = id_str[:len(id_str)//2], id_str[len(id_str)//2:]
                if idl == idr:
                    invalid_ids.append(int(id_int))
                    #print(f"{id_int = } {idl = } {idr = }")
        
    return sum(invalid_ids)


@time_duration
def part2(l1: list) -> int:
    def is_invalid(id_str: str) -> bool:
        if len(id_str) < 2:
            return False
        
        for n_slices in range(2, len(id_str)+1):
            if len(id_str) % n_slices != 0:
                continue
            
            base = id_str[:len(id_str) // n_slices]
            for i in range(1, n_slices):
                next_value = id_str[len(id_str) // n_slices * i: len(id_str) // n_slices * (i+1)]
                if base != next_value:
                    break
            else:
                #print(f"{id_str = } {base = } {n_slices = }")
                return True

        return False
    
    invalid_ids = []
    for (id1, id2) in l1:
        id1, id2 = int(id1), int(id2)
        for id_int in range(id1, id2 + 1):
            id_str = str(id_int)
            if is_invalid(id_str):
                invalid_ids.append(int(id_int))
        
    return sum(invalid_ids)


@time_duration
def run_all():
    l1 = parse()

    p1 = part1(l1)
    p2 = part2(l1)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
