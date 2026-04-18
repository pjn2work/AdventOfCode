import sys
import os
import re
from itertools import combinations
from collections import deque

# Add project root to sys.path
CWD = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(CWD, "../..")))

from utilities import time_duration


def _parse_line(line: str) -> tuple[str, list[tuple[int, ...]], tuple[int, ...]]:
    match = re.search(r"\[([.#]+)\]\s+((?:\([\d,]+\)\s*)+)\{([\d,]+)\}", line)

    # Extracting string from [.##.]
    lights_goal = match.group(1)
    # Extracting tuples from (3) (1,3) ...
    buttons = [tuple(map(int, t.split(','))) for t in re.findall(r"\(([\d,]+)\)", match.group(2))]
    # Extracting numbers from {3,5,4,7}
    joltage = tuple(map(int, match.group(3).split(',')))

    return lights_goal, buttons, joltage


@time_duration
def parse() -> list:
    with open(os.path.join(CWD, "input.txt"), mode="r", encoding="utf-8") as f:
        return [_parse_line(line.strip()) for line in f]


def convert_lights_goal_to_int(light_goal: str) -> int:
    result = 0
    for light in light_goal[::-1]:
        result = (result << 1) + (1 if light == '#' else 0)
    return result


def convert_button_to_int(button: tuple[int]) -> int:
    return sum(2**light_pos for light_pos in button)


def calc1(
        lights_initial_int: int,
        lights_goal_int: int,
        buttons_to_press_int: list[int],
        visited_light_states: dict[int, tuple[int, ...]],
        buttons_pressed_counter: tuple[int, ...],
) -> tuple[int, ...] | None:
    # Goal reached
    if lights_initial_int == lights_goal_int:
        return buttons_pressed_counter

    results = []
    for button_pos, button_int in enumerate(buttons_to_press_int):
        # New lights configuration when this button was pressed
        lights_new_int = lights_initial_int ^ button_int

        # Optimization: avoid going back to the same state
        buttons_pressed_counter_new = tuple(
            times_button_was_pressed + 1 if pos == button_pos else times_button_was_pressed
            for pos, times_button_was_pressed in enumerate(buttons_pressed_counter)
        )

        # Exceeded maximum clicks for this button (only 0 or 1 needed for toggling)
        if buttons_pressed_counter_new[button_pos] > 1:
            continue

        # Lights On/Off configuration already repeated? otherwise save it
        if lights_new_int in visited_light_states:
            if sum(buttons_pressed_counter_new) < sum(visited_light_states[lights_new_int]):
                visited_light_states[lights_new_int] = buttons_pressed_counter_new
            else:
                continue
        else:
            visited_light_states[lights_new_int] = buttons_pressed_counter_new

        # Continue searching for the goal
        result_with_button = calc1(lights_new_int, lights_goal_int, buttons_to_press_int, visited_light_states, buttons_pressed_counter_new)
        if result_with_button:
            results.append(result_with_button)

    if results:
        return min(results, key=sum)
    return None


def calc2(
        buttons_to_press: list[tuple[int, ...]],
        buttons_pressed: list[int],
        visited_joltage_states: dict[tuple[int, ...], list[int]], # Changed to dict for memoization
        current_joltage: list[int],
        joltage_max: tuple[int, ...],
) -> list[int] | None: # Changed return type hint
    # Goal reached
    if tuple(current_joltage) == joltage_max: # Convert to tuple for comparison
        return buttons_pressed

    results = []
    for button_pos, button in enumerate(buttons_to_press):
        # Check if pressing the button will exceed the maximum joltage
        exceed = False
        new_joltage = current_joltage.copy()
        for light_idx in button: # Iterate through light indices affected by the button
            new_joltage[light_idx] += 1
            if new_joltage[light_idx] > joltage_max[light_idx]:
                exceed = True
                break
        if exceed:
            continue

        # Since button didn't exceed joltage, it's possible to press it
        new_buttons_pressed = buttons_pressed.copy()
        new_buttons_pressed[button_pos] += 1

        new_joltage_tuple = tuple(new_joltage) # Convert to tuple for dict key

        # Optimization: avoid going back to the same state if a better path exists
        if new_joltage_tuple in visited_joltage_states:
            # If we found a path to this joltage state with fewer total button presses
            if sum(new_buttons_pressed) < sum(visited_joltage_states[new_joltage_tuple]):
                visited_joltage_states[new_joltage_tuple] = new_buttons_pressed
            else:
                continue # This path is not better
        else:
            visited_joltage_states[new_joltage_tuple] = new_buttons_pressed

        # Continue searching for the goal
        result_with_button = calc2(buttons_to_press, new_buttons_pressed, visited_joltage_states, new_joltage, joltage_max)
        if result_with_button:
            results.append(result_with_button)

    if results:
        return min(results, key=sum) # sum() works on list[int]
    return None


@time_duration
def part1(data: list) -> int:
    number_button_presses = 0
    for lights_goal, buttons, _ in data:
        lights_goal_int = convert_lights_goal_to_int(lights_goal)
        buttons_to_press_int = [convert_button_to_int(button) for button in buttons]
        buttons_pressed_n_times = tuple(0 for _ in range(len(buttons)))

        min_button_press = calc1(0, lights_goal_int, buttons_to_press_int, {0: buttons_pressed_n_times}, buttons_pressed_n_times)
        if min_button_press:
            number_button_presses += sum(min_button_press)

    return number_button_presses


@time_duration
def part2(data: list) -> int:
    number_button_presses = 0
    for _, buttons_to_press, joltage_max in data:
        # Initial state: current_joltage is all zeros, no buttons pressed
        initial_current_joltage = [0 for _ in range(len(joltage_max))]
        initial_buttons_pressed = [0 for _ in range(len(buttons_to_press))]

        # Initialize visited_joltage_states with the initial state
        # Key: tuple(initial_current_joltage), Value: initial_buttons_pressed
        visited_joltage_states = {tuple(initial_current_joltage): initial_buttons_pressed}

        result = calc2(
            buttons_to_press=buttons_to_press,
            buttons_pressed=initial_buttons_pressed,
            visited_joltage_states=visited_joltage_states, # Pass the dict
            current_joltage=initial_current_joltage,
            joltage_max=joltage_max
        )
        if result: # Check if result is not None
            number_button_presses += sum(result) # Sum the list directly
        else:
            # Handle the case where no solution is found for a given input
            print(f"No solution found for buttons: {buttons_to_press}, joltage_max: {joltage_max}")
    return number_button_presses


@time_duration
def run_all():
    data = parse()

    p1 = part1(data)
    p2 = part2(data)

    print(f"Result for {p1 = }")
    print(f"Result for {p2 = }")


if __name__ == "__main__":
    run_all()
