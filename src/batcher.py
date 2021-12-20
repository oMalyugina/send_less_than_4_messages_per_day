import datetime
from collections import defaultdict
from fastapi import FastAPI
from typing import Dict, List

from dto.batcher_dto import ResetTimerDTO, UserMessage
from messages_delay_counter import MessagesDelayCounter
from simulation_timer import SimulationTimer

class Queue:

    def __init__(self):
        self.message_queues = defaultdict(list)  # dict {user:messages}
        self.delays = []

    def push_message(self, obj: UserMessage) -> None:
        # print("push_message(): obj=" + str(obj))
        self.message_queues[obj.to_id].append(obj)

    def send_all(self) -> Dict[str, List[UserMessage]]:
        # for to_id, messages in self.message_queues.items():
        #     if len(messages) == 1:
        #         print(f"{messages[0].from_name} went on a tour")
        #     elif len(messages) == 2:
        #         print(f"{messages[0].from_name} and {len(messages) - 1} other went on a tour")
        #     elif len(messages) >= 2:
        #         print(f"{messages[0].from_name} and {len(messages) - 1} others went on a tour")
        result = self.message_queues
        self.message_queues = defaultdict(list)
        return result


queue = Queue()
simulation_timer = SimulationTimer(datetime.datetime.now(), datetime.datetime.now(), 1)
messages_delay_counter = MessagesDelayCounter()

app = FastAPI()


@app.post("/message")
async def push_message(obj: UserMessage) -> None:
    queue.push_message(obj)


@app.post("/batch")
async def send():
    current_time = simulation_timer.get_current_virtual_time()
    messages_dict = queue.send_all()
    for to_id, messages in messages_dict.items():
        messages_delay_counter.update_with_messages(current_time, messages)
    delay_stats = messages_delay_counter.delay_stats()
    # print(delay_stats)
    return delay_stats


@app.post("/timer")
async def reset_timer(obj: ResetTimerDTO):
    simulation_timer.reset(obj.real_time_start, obj.virtual_time_start, obj.multiplier)
    print("Current simulation time: {}".format(str(simulation_timer.get_current_virtual_time())))
    return obj
