import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from utilities import time_duration
from functools import lru_cache
import math, re


extra_cards = dict()


@time_duration
def part1() -> int:
   num = re.compile(r"\d+")
   p1 = 0

   with open("input.txt", mode="r", encoding="utf-8") as f:
      for line in f:
         txt = line.strip().split(":")
         card = int(num.search(txt[0]).group())
         _numbers = txt[1].split("|")

         win_numbers = set([int(n.group()) for n in num.finditer(_numbers[0])])
         my_numbers = [int(n.group()) for n in num.finditer(_numbers[1])]

         wins = sum((1 for n in win_numbers if n in my_numbers))
         if wins:
            p1 += int(math.pow(2, wins-1))
         
         # for part 2
         extra_cards[card] = [card + 1 + g for g in range(wins)]

   return p1


@time_duration
def part2():
   
   @lru_cache
   def get_extra_cards_of(card):
      return 1 + sum([get_extra_cards_of(c) for c in extra_cards[card]])

   total_cards = 0
   for card in extra_cards:
      total_cards += get_extra_cards_of(card)
   
   return total_cards


@time_duration
def all():
   p1, p2 = part1(), part2()
   print(f"Result for {p1 = }")
   print(f"Result for {p2 = }")


if __name__ == "__main__":
   all()
