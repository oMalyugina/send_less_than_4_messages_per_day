import datetime
import time


class SimulationTimer:
    real_time_start: datetime.datetime
    virtual_time_start: datetime.datetime
    multiplier: int

    def __init__(self, real_time_start: datetime.datetime, virtual_time_start: datetime.datetime, multiplier=1200):
        self.reset(real_time_start, virtual_time_start, multiplier)

    def reset(self, real_time_start: datetime.datetime, virtual_time_start: datetime.datetime, multiplier=1200):
        self.real_time_start = real_time_start
        self.virtual_time_start = virtual_time_start
        self.multiplier = multiplier

    def get_current_virtual_time(self):
        real_now = datetime.datetime.now()
        real_time_delta = real_now - self.real_time_start
        virtual_time_delta = datetime.timedelta(seconds=self.multiplier * real_time_delta.total_seconds())

        return self.virtual_time_start + virtual_time_delta

    def get_real_seconds_delay_to_virtual_time(self, virtual_time: datetime.datetime):
        current_virtual_time = self.get_current_virtual_time()
        seconds = (virtual_time - current_virtual_time).seconds / self.multiplier
        return max(seconds, 0)

    def __str__(self):
        return "<SimulationTimer real={}, virtual={}, mul={}>".format(str(self.real_time_start),
                                                                      str(self.virtual_time_start), self.multiplier)


if __name__ == "__main__":
    st = SimulationTimer(
        datetime.datetime.now(),
        datetime.datetime(year=2017, day=1, month=8, hour=0, minute=0, second=0)
    )

    print(st.virtual_time_start)

    time.sleep(1)
    print(st.get_current_virtual_time())
