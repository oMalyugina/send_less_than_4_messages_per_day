import datetime
from typing import List

from dto.batcher_dto import UserMessage


class MessagesDelayCounter:

    def __init__(self):
        self.delays = []

    def update_with_messages(self, current_time: datetime.datetime, messages: List[UserMessage]):
        for message in messages:
            message_time = datetime.datetime.strptime(message.timestamp, '%Y-%m-%d  %H:%M:%S')
            delay = (current_time - message_time).seconds / 60
            print(
                "New delay added: current_time={}, message_time={}, delay={} minutes".format(current_time, message_time,
                                                                                             delay))
            self.delays.append(delay)

    def reset(self):
        self.delays = []

    def delay_stats(self):
        if len(self.delays) == 0:
            return {}
        number_messages = len(self.delays)
        sum_delays = sum(self.delays)
        return {"sum": sum_delays, "mean": sum_delays / number_messages}
