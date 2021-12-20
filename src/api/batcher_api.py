import requests


def post_pop_batch(host: str):
    response = requests.post(host + "/batch")
    return response.text
