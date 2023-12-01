import re


# Part 1 ----------------------------

def get_first_last_number(txt: str) -> (int, int, int, int):
   res = re.search("(\\d).*(\\d)", txt)
   
   if res is None:
       res = re.search("(\\d)", txt)
       if res is None:
          return None, None, None, None
       return res.span()[0], int(res.group(1)), res.span()[0], int(res.group(1))
   
   return res.span()[0], int(res.group(1)), res.span()[1]-1, int(res.group(2))


# Part 2 ----------------------------

def index_of(txt: str, s: str) -> int | None:
   try:
      return txt.index(s)
   except ValueError:
      return None

def rindex_of(txt: str, s: str) -> int | None:
   try:
      return txt.rindex(s)
   except ValueError:
      return None

numbers = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")

def get_first_last_number_textual(txt: str) -> (int, int, int, int):
   vi1, vn1, vi2, vn2 = get_first_last_number(txt)

   for n, number in enumerate(numbers, 1):
      ti1 = index_of(txt, number)
      ti2 = rindex_of(txt, number)
      if ti1 is not None and (vi1 is None or ti1 < vi1):
         vi1, vn1 = ti1, n
      if ti2 is not None and (vi2 is None or ti2 > vi2):
         vi2, vn2 = ti2, n

   return vi1, vn1, vi2, vn2


# Main ------------------------------

def parser(method) -> int:
   res = 0
   with open("input.txt", mode="r", encoding="utf-8") as f:
      for line in f:
         _, n1, _, n2 = method(line.strip())
         if n1 is not None:
            res += n1*10 + n2
   return res


if __name__ == "__main__":
   print("Result for part1:", parser(get_first_last_number))
   print("Result for part2:", parser(get_first_last_number_textual))
