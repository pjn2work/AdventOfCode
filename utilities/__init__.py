from utilities.set_range import *
from utilities.tables import *
from utilities.time_duration_wrapper import time_duration
from utilities.geometry import Polygon

from functools import reduce


mul = lambda x,y: x*y
def prod(iter):
   return reduce(mul, iter, 1)


def if_exception_return_none(method, *args):
   try:
      return method(*args)
   except Exception:
      return None
