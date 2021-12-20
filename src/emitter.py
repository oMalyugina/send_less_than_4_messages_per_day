import time

import pandas as pd
import os
import datetime
import requests
from simulation_timer import SimulationTimer


class Sender:
    data = None
    sender_adress = None

    def __init__(self):
        path_to_csv = os.environ['DATA']
        self.sender_adress = os.environ["BATCHER_HOST"]
        data = pd.read_csv(path_to_csv, names=["timestamp", "to_id", "from_id", "from_name"])

        data["timestamp"] = data["timestamp"].apply(
            lambda string: datetime.datetime.strptime(string, '%Y-%m-%d  %H:%M:%S'))

        data.sort_values(by="timestamp", inplace=True)
        self.data = data

    def send(self, row: dict) -> None:
        body = {
            'timestamp': row["timestamp"].strftime('%Y-%m-%d  %H:%M:%S'),
            'to_id': row["to_id"],
            'from_id': row["from_id"],
            'from_name': row["from_name"]
        }

        response = requests.post(self.sender_adress + "/message", json=body)
        # print(response.text)

    def send_reset_timer(self, simulation_timer: SimulationTimer):
        body = {
            'real_time_start': str(simulation_timer.real_time_start),
            'virtual_time_start': str(simulation_timer.virtual_time_start),
            'multiplier': simulation_timer.multiplier
        }
        response = requests.post(self.sender_adress + "/timer", json=body)
        # print(response.text)

    def simulate(self):
        first_timestamp: datetime.datetime = self.data.iloc[0].timestamp

        st = SimulationTimer(datetime.datetime.now(),
                             datetime.datetime(year=first_timestamp.year, day=first_timestamp.day,
                                               month=first_timestamp.month, hour=0, minute=0, second=0),
                             60 * 60 * 3
                             )

        print("Current virtual time: {}".format(st.get_current_virtual_time()))
        self.send_reset_timer(st)
        current_time = st.get_current_virtual_time()
        print("current_time: {}".format(current_time))
        for row in self.data.to_dict(orient="records"):
            time_to_send = row["timestamp"]
            print("time_to_send: {}".format(time_to_send))
            while time_to_send > current_time:
                # to_sleep = st.get_real_seconds_delay_to_virtual_time(time_to_send)
                # print("to_sleep: {}".format(to_sleep))
                # time.sleep(to_sleep)
                time.sleep(0.001)
                current_time = st.get_current_virtual_time()
                # print("current_time: {}".format(current_time))
            self.send(row)


if __name__ == "__main__":
    sender = Sender()
    sender.simulate()
