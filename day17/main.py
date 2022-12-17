from dataclasses import dataclass
from itertools import cycle
from utilities import SetRange1D


def parser(method, **kwargs):
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            method(line.strip(), **kwargs)


@dataclass
class Puzzle:
    jet_cycle: cycle
    pit: list[SetRange1D]
    pit_height: int = 0
    current_rock_bottom_height: int = 0


def read_input(line: str, p: Puzzle):
    p.jet_cycle = cycle(enumerate(line))


"""
shape L
 col 012345678
-----+-------|
row 2|    #  |
row 1|    #  |
row 0|  ###  |
"""
PIT_WIDTH = 7
SR = 4  # new Rock starting row -> above last rock or ground
SC = 2  # new Rock starting column
shape_minus = [SetRange1D(1, 4) >> SC]
shape_plus = [SetRange1D(2, 2) >> SC, SetRange1D(1, 3) >> SC, SetRange1D(2, 2) >> SC]
shape_l = [SetRange1D(1, 3) >> SC, SetRange1D(3, 3) >> SC, SetRange1D(3, 3) >> SC]
shape_i = [SetRange1D(1, 1) >> SC, SetRange1D(1, 1) >> SC, SetRange1D(1, 1) >> SC, SetRange1D(1, 1) >> SC]
shape_square = [SetRange1D(1, 2) >> SC, SetRange1D(1, 2) >> SC]


def build_pit_walls(p: Puzzle, n_rows: int):
    for _ in range(n_rows):
        p.pit.append(SetRange1D(0, 0).add(PIT_WIDTH+1, PIT_WIDTH+1))


def colliding_with_other_rock_or_wall(rock: list[SetRange1D], p: Puzzle) -> bool:
    for r in range(len(rock)):
        if p.pit[p.current_rock_bottom_height + r].get_inner_join(rock[r]):
            return True
    return False


def move_rock_with_jet(jet: str, rock: list[SetRange1D], p: Puzzle) -> list[SetRange1D]:
    new_rock = [r.copy() for r in rock]
    for r in new_rock:
        if jet == ">":
            r >> 1
        else:
            r << 1

    if colliding_with_other_rock_or_wall(new_rock, p):
        return rock
    return new_rock


def solve(p: Puzzle, total_rocks: int) -> int:
    rocks_cycle = cycle(enumerate([shape_minus, shape_plus, shape_l, shape_i, shape_square]))
    seen_block = dict()
    last_floor_at, skipping_ys = 0, 0
    pattern_not_found = True
    for rock_id, rock in rocks_cycle:
        rock = [r.copy() for r in rock]
        p.current_rock_bottom_height = p.pit_height + SR
        if (t := p.current_rock_bottom_height + len(rock) - len(p.pit)) > 0:
            build_pit_walls(puzzle, t)

        while True:
            jet_id, jet = next(p.jet_cycle)
            rock = move_rock_with_jet(jet, rock, p)
            p.current_rock_bottom_height -= 1
            if colliding_with_other_rock_or_wall(rock, p):
                p.current_rock_bottom_height += 1
                for r in range(len(rock)):
                    p.pit[p.current_rock_bottom_height + r] += rock[r]
                p.pit_height = max(p.current_rock_bottom_height + len(rock)-1, p.pit_height)

                if pattern_not_found:
                    # check for new floor
                    for y in range(p.current_rock_bottom_height, p.current_rock_bottom_height + len(rock)):
                        if p.pit[y].get_occupied() == [(0, 8)]:
                            # get block between floors
                            block = tuple(map(tuple, p.pit[last_floor_at:y]))
                            key = (block, rock_id, jet_id)
                            if key in seen_block:
                                print(f"DUPLICATE PATTERN AT: {y=:,}, block_size={len(block):,} {p.pit_height=:,}, were missing rocks={total_rocks:,}")
                                missing_rocks_before, last_y = seen_block[key]
                                period = missing_rocks_before - total_rocks
                                y_diff = y - last_y
                                iterations = total_rocks // period
                                skipping_ys = iterations * y_diff
                                total_rocks -= iterations * period
                                print(f"   -- {skipping_ys=:,}, {period=:,}, {iterations=:,}, {total_rocks=:,} now missing")
                                pattern_not_found = False
                                break

                            seen_block[key] = (total_rocks, y)
                            last_floor_at = y
                            break

                break  # break while -> NEXT ROCK

        total_rocks -= 1
        if total_rocks <= 0:
            break

    return p.pit_height + skipping_ys


if __name__ == "__main__":
    puzzle = Puzzle(jet_cycle=None, pit=[SetRange1D(0, PIT_WIDTH + 1)])
    parser(read_input, p=puzzle)
    print("Answer 1:", solve(p=puzzle, total_rocks=2_022))

    puzzle = Puzzle(jet_cycle=None, pit=[SetRange1D(0, PIT_WIDTH + 1)])
    parser(read_input, p=puzzle)
    print("Answer 2:", solve(p=puzzle, total_rocks=1_000_000_000_000))
