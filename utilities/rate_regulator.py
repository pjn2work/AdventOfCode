import time
from datetime import datetime, timedelta
from typing import Union


class RateRegulator:
  def __init__(self, rps: float = 1, rpm: float = None):
    if not (rps or rpm):
      raise ValueError("Either new_rps or new_rpm must be provided.")

    self._max_rpm: float = rpm if rpm else rps * 60
    self._wait_time_sec: timedelta = timedelta(seconds=60 / self._max_rpm)
    self._next_time: datetime = datetime.now()

  def update_rate(self, new_rps: float = None, new_rpm: float = None) -> None:
    if not (new_rps or new_rpm):
      raise ValueError("Either new_rps or new_rpm must be provided.")

    self._max_rpm = new_rpm if new_rpm else new_rps * 60
    self._wait_time_sec = timedelta(seconds=60 / self._max_rpm)
    self._next_time = datetime.now()

  def get_max_rpm(self) -> float:
    return self._max_rpm

  def get_wait_time_sec(self) -> timedelta:
    return self._wait_time_sec

  def wait_for_next(self) -> None:
    sleep_sec = (self._next_time - datetime.now()).total_seconds()
    if sleep_sec > 0:
      time.sleep(sleep_sec)
      self._next_time += self._wait_time_sec
    else:
      self._next_time = datetime.now() + self._wait_time_sec

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

  print("timer(timedelta(sec=0.5))".center(40, "-"))

  for i in regulator.timer(timedelta(seconds=0.5)):
    print(f"Action {i} at {datetime.now()}")
