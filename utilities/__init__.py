from utilities.set_range import *
from utilities.time_duration_wrapper import time_duration

from functools import reduce


mul = lambda x,y: x*y
def prod(iter):
   return reduce(mul, iter, 1)
