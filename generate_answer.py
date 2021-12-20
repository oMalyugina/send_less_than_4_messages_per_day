import pandas as pd
import datetime
import numpy as np
from collections import defaultdict
from typing import List, Dict
import argparse


def send(messages_to_send: Dict[str, List[dict]], time_when_print: datetime.datetime) -> List[List]:
    rows_in_csv = []
    for to_id, messages in messages_to_send.items():
        if len(messages) == 0:
            continue
        if len(messages) == 1:
            string = f"{messages[0]['from_name']} went on a tour"
        elif len(messages) == 2:
            string = f"{messages[0]['from_name']} and {len(messages) - 1} other went on a tour"
        else:
            string = f"{messages[0]['from_name']} and {len(messages) - 1} others went on a tour"
        row_to_answer = [time_when_print.strftime(time_format), messages[0]["time"].strftime(time_format),
                         len(messages), to_id, string]
        rows_in_csv.append(row_to_answer)
    return rows_in_csv


def compute_mean_message_pro_day(data: pd.DataFrame) -> Dict[str, float]:
    mean_freq = {}
    data["date"] = data["timestamp"].apply(lambda dt: dt.date())
    for user_id, group in data.groupby(["to_id"]):
        mail_pro_day = group.groupby(["date"]).size().values
        # print(mail_pro_day)
        mean_freq[user_id] = np.mean(mail_pro_day)
    return mean_freq


# method4
def method4(data: pd.DataFrame, mean_freq: Dict[str, float]) -> List[list]:
    printed_today = defaultdict(lambda: 0)
    next_dt = datetime.datetime(year=2017, month=8, day=1, hour=22, minute=0, second=0)
    answer = []
    messages_to_send = defaultdict(list)

    for row in data.to_dict(orient="records"):
        if row['timestamp'] > next_dt:
            answer.extend(send(messages_to_send, next_dt))
            next_dt += datetime.timedelta(days=1)
            messages_to_send = defaultdict(list)
            printed_today = defaultdict(lambda: 0)

        current_id = row["to_id"]
        if printed_today[current_id] == 3:
            messages_to_send[current_id].append(
                {"from_id": row['from_id'], "time": row['timestamp'], "from_name": row['from_name']})
            continue
        if current_id not in mean_freq or mean_freq[current_id] < 3:
            dict_to_send = {
                current_id: [{"from_id": row['from_id'], "time": row['timestamp'], "from_name": row['from_name']}]}
            answer.extend(send(dict_to_send, row['timestamp']))
            printed_today[current_id] += 1
        else:
            messages_to_send[current_id].append(
                {"from_id": row['from_id'], "time": row['timestamp'], "from_name": row['from_name']})
            if len(messages_to_send[current_id]) > mean_freq[current_id] / 4:
                dict_to_send = {current_id: messages_to_send[current_id]}
                answer.extend(send(dict_to_send, row['timestamp']))
                messages_to_send[current_id] = []
                printed_today[current_id] += 1

    answer.extend(send(messages_to_send, next_dt))
    return answer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='provide path to source csv and path where you want to save answer.')
    parser.add_argument('--source', type=str, dest="path_to_source", required=True)
    parser.add_argument('--result', type=str, dest='path_to_res', required=True)
    args = parser.parse_args()

    data = pd.read_csv(args.path_to_source, names=["timestamp", "to_id", "from_id", "from_name"])
    time_format = '%Y-%m-%d  %H:%M:%S'
    data["timestamp"] = data["timestamp"].apply(lambda string: datetime.datetime.strptime(string, time_format))
    data.sort_values(by="timestamp", inplace=True)

    # In ideal world, mean_freq should be computed on train dataset, method4 should be run on test dataset.
    # because I should generate answers for all data, I compute all on full dataset.
    # it is not good.
    mean_freq = compute_mean_message_pro_day(data)
    answer = method4(data, mean_freq)
    answer = pd.DataFrame(answer,
                          columns=["notification_sent", "timestamp_first_tour", "tours", "receiver_id", "message"])

    assert sum(answer.tours.values) == len(data)
    answer.to_csv(args.path_to_res)

    print(f"answer saved to {args.path_to_res}")

