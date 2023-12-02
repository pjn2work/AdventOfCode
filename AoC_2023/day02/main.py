import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from utilities import time_duration, prod


# Part 1 ----------------------------

def get_cubes(line: str) -> dict:
   # {"red": 0, "green": 0, "blue": 0}
   res = dict()
   for cubes_color in line.split(","):
      qtt_color = cubes_color.strip().split(" ")
      qtt, color = int(qtt_color[0]), qtt_color[1]
      
      res[color] = res.get(color, 0) + qtt
   
   return res


def get_number_cubes(line: str) -> list[dict]:
   return [get_cubes(draw) for draw in line.split(";")]


def validate_maxs(draws: list[dict], max_cubes: dict):
   for draw in draws:
      for color, qtt in draw.items():
         if qtt > max_cubes[color]:
            return False
   return True


# Part 2 ----------------------------

def get_fewest_cubes(draws: list[dict]) -> dict:
   # {"red": 0, "green": 0, "blue": 0}
   min_draw = dict()
   for draw in draws:
      for color, qtt in draw.items():
         if qtt > min_draw.get(color, 0):
            min_draw[color] = qtt
   return min_draw


# Main ------------------------------

@time_duration(name="Calculate part1 and part2")
def parser() -> (int, int):
   max_cubes = {"red": 12, "green": 13, "blue": 14}
   valid_games_sum, sum_power_sets = 0, 0

   with open("input.txt", mode="r", encoding="utf-8") as f:
      for line in f:
         txt = line.strip().split(":")

         game = int(txt[0].split(" ")[1])
         draws = get_number_cubes(txt[1])

         # part 1
         if validate_maxs(draws, max_cubes):
            valid_games_sum += game

         # part 2
         fewest = get_fewest_cubes(draws)
         sum_power_sets += prod([x for x in fewest.values()])
         
   return valid_games_sum, sum_power_sets


if __name__ == "__main__":
   valid_games_sum, sum_power_sets = parser()
   print("Result for part1:", valid_games_sum)
   print("Result for part2:", sum_power_sets)
