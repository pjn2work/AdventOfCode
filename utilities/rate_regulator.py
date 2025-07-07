import time
from datetime import datetime, timedelta
from typing import Union


class RateRegulator:
  def __init__(self, rps: float = 1, rpm: float = None):
    if not (rps or rpm):
      raise ValueError("Either new_rps or new_rpm must be provided.")

    self._max_rpm: float = rpm if rpm else rps * 60
    self._wait_time_ns: float = 60_000_000_000 / self._max_rpm
    self._next_time: float = time.perf_counter_ns()

  def update_rate(self, new_rps: float = None, new_rpm: float = None) -> None:
    if not (new_rps or new_rpm):
      raise ValueError("Either new_rps or new_rpm must be provided.")

    self._max_rpm = new_rpm if new_rpm else new_rps * 60
    self._wait_time_ns = 60_000_000_000 / self._max_rpm
    self._next_time = time.perf_counter_ns()

  def get_max_rpm(self) -> float:
    return self._max_rpm

  def get_max_rps(self) -> float:
    return self._max_rpm / 60

  def get_wait_time_sec(self) -> float:
    return self._wait_time_ns / 1_000_000_000

  def wait_for_next(self) -> None:
    _now = time.perf_counter_ns()
    sleep_ns = self._next_time - _now
    if sleep_ns > 0:
      time.sleep(sleep_ns / 1_000_000_000)
      self._next_time += self._wait_time_ns
    else:
      self._next_time = _now + self._wait_time_ns

  def range(self, max_iterations: int = None):
    if max_iterations is not None and max_iterations < 0:
      raise ValueError("max_iterations must be a positive integer or None.")

    counter = 0
    while max_iterations is None or counter < max_iterations:
      self.wait_for_next()
      yield counter
      counter += 1

  def timer(self, duration: Union[timedelta, int, float]):
    """Wait for a specified number of seconds (if int)."""
    if isinstance(duration, (int, float)):
      duration = timedelta(seconds=duration)
    elif not isinstance(duration, timedelta):
      raise TypeError("duration must be an int, float or timedelta.")

    counter: int = 0
    end_time = datetime.now() + duration
    while datetime.now() < end_time:
      self.wait_for_next()
      yield counter
      counter += 1

  def __repr__(self) -> str:
    if self._max_rpm < 60:
      return f"RateRegulator(rpm={self.get_max_rpm():_.2f})"
    return f"RateRegulator(rps={self.get_max_rps():_.2f})"

  def __str__(self) -> str:
    if self._max_rpm < 60:
      return f"{self.get_max_rpm():_.2f} RPM, every {self.get_wait_time_sec():_.3f} sec"
    return f"{self.get_max_rps():_.2f} RPS, every {self.get_wait_time_sec()*1000:_.3f} ms"


# Example usage
if __name__ == "__main__":
  regulator = RateRegulator(rps=10)
  print(f"Executing {regulator.get_max_rpm()} RPM, every {regulator.get_wait_time_sec()}")

  for i in range(9):
    regulator.wait_for_next()
    print(f"Action {i} at {datetime.now()}")

  print("range(6)".center(40, "-"))

  for i in regulator.range(6):
    print(f"Action {i} at {datetime.now()}")

  print("range() stop at 2".center(40, "-"))

  for i in regulator.range():
    print(f"Action {i} at {datetime.now()}")
    if i == 2:
      break

  print("timer(1.5) sec".center(40, "-"))

  for i in regulator.timer(1.5):
    print(f"Action {i} at {datetime.now()}")

  regulator.update_rate(new_rps=20_000)
  print(f"{regulator} for 1.0 sec ".center(80, "-"))
  _counter = 0
  for i in regulator.timer(timedelta(seconds=1.0)):
    _counter += 1
  print(f"Total executions {_counter:_}, expected: 20_000")
