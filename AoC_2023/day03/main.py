import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from utilities import time_duration, prod
from dataclasses import dataclass


@dataclass
class ElementPos:
   row: int
   col1: int
   col2: int
   value: int | str


@dataclass
class PuzzleDetails:
   rows: int
   cols: int
puzzle_details = PuzzleDetails(0, 0)


# Part 1 ----------------------------

def is_symbol_in_row_range(row: int, col1: int, col2: int, symbols: list[ElementPos]) -> bool:
   if 0 <= row <= puzzle_details.rows:
      for symbol in symbols:
         if symbol.row == row and col1 <= symbol.col1 <= col2:
            return True
         if symbol.row > row:
            break
   
   return False


@time_duration(name="part 1")
def sum_numbers_adjacent_to_symbols(numbers: list[ElementPos], symbols: list[ElementPos]) -> int:
   sum_valid_numbers = 0
   for number in numbers:
      if is_symbol_in_row_range(number.row-1, number.col1-1, number.col2+1, symbols) or \
         is_symbol_in_row_range(number.row, number.col1-1, number.col2+1, symbols) or \
         is_symbol_in_row_range(number.row+1, number.col1-1, number.col2+1, symbols):
         sum_valid_numbers += number.value
   
   return sum_valid_numbers


# Part 2 ----------------------------

def get_numbers_in_row_range(row: int, col1: int, col2: int, numbers: list[ElementPos]) -> list[ElementPos]:
   res = list()
   if 0 <= row <= puzzle_details.rows:
      for number in numbers:
         if number.row == row and number.col1 <= col2 and number.col2 >= col1:
            res.append(number)
         if number.row > row:
            break
   
   return res


@time_duration(name="part 2")
def sum_numbers_adjacent_to_gears(numbers: list[ElementPos], symbols: list[ElementPos]) -> int:
   sum_valid_gears = 0
   for symbol in symbols:
      if symbol.value == "*":
         numbers_per_rows = [get_numbers_in_row_range(symbol.row+i-1, symbol.col1-1, symbol.col2+1, numbers) for i in range(3)]
         numbers_per_rows = [e.value for x in numbers_per_rows for e in x]
         
         if len(numbers_per_rows) >= 2:
            sum_valid_gears += prod(numbers_per_rows)
   
   return sum_valid_gears


# Main ------------------------------

@time_duration
def parser() -> (list[ElementPos], list[ElementPos]):
   numbers = list()
   symbols = list()
   row = 0
   number = None

   with open("input.txt", mode="r", encoding="utf-8") as f:
      for line in f:
         
         for i, c in enumerate(line.strip()):
            # build numbers
            if "0" <= c <= "9":
               if number is None:
                  number = ElementPos(row=row, col1=i, col2=i, value=int(c))
               else:
                  number.col2 = i
                  number.value = number.value*10 + int(c)
            else:
               # add number
               if number is not None:
                  numbers.append(number)
                  number = None

               # add symbol
               if c != ".":
                  symbols.append(ElementPos(row=row, col1=i, col2=i, value=c))

         # add number
         if number is not None:
            numbers.append(number)
            number = None

         puzzle_details.rows = row
         puzzle_details.cols = i

         row += 1

   return numbers, symbols


@time_duration
def all():
   numbers, symbols = parser()

   part1 = sum_numbers_adjacent_to_symbols(numbers, symbols)
   part2 = sum_numbers_adjacent_to_gears(numbers, symbols)

   print(f"Result for {part1 = }")
   print(f"Result for {part2 = }")


if __name__ == "__main__":
   all()
