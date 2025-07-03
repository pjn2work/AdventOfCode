import time
from datetime import datetime, timedelta


class RateRegulator:
  def __init__(self, rps: float = 1, rpm: float = None):
    self._max_rpm: float = rpm if rpm else rps * 60
    self._wait_time_sec: timedelta = timedelta(seconds=60/self._max_rpm)
    self._next_time: datetime = datetime.now()

  def update_rate(self, new_rps: float = None, new_rpm: float = None) -> None:
    if not new_rps and not new_rpm:
      raise ValueError("Either new_rps or new_rpm must be provided.")

    self._max_rpm = new_rpm if new_rpm else new_rps * 60
    self._wait_time_sec = timedelta(seconds=60 / self._max_rpm)
    self._next_time = datetime.now()

  def get_max_rpm(self) -> float:
    return self._max_rpm

  def get_wait_time_sec(self) -> timedelta:
    return self._wait_time_sec

  def wait_for_next(self):
    sleep_sec = (self._next_time - datetime.now()).total_seconds()
    if sleep_sec > 0:
      time.sleep(sleep_sec)
      self._next_time += self._wait_time_sec
    else:
      self._next_time = datetime.now() + self._wait_time_sec


# Example usage
if __name__ == "__main__":
  regulator = RateRegulator(rps=10)
  print(f"Executing {regulator.get_max_rpm()} RPM, every {regulator.get_wait_time_sec()}")
  for i in range(10):
    regulator.wait_for_next()
    print(f"Action {i} at {datetime.now()}")
