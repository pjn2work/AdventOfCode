import time
from types import MethodType


def time_duration(_func=None, *, name: str = ""):
    class RunMethod:
        def __init__(self, func):
            self.func = func

        def __call__(self, *args, **kwargs):
            t1 = time.perf_counter()
            res = self.func(*args, **kwargs)
            t2 = time.perf_counter()
            print(f"{name or self.func.__name__} took: {t2-t1:0.6f} sec")
            return res

        def __get__(self, instance, owner):
            return self if instance is None else MethodType(self, instance)

    if _func is None:
        return RunMethod
    else:
        return RunMethod(_func)
