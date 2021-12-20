FROM python:3.7.2-slim as base

WORKDIR /code

RUN apt update && apt install -y curl

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -U pip
RUN pip install -r /tmp/requirements.txt

COPY src src
WORKDIR src

FROM base as batcher

CMD uvicorn --host 0.0.0.0 --log-level warning batcher:app

FROM base as emitter

CMD ["python", "-u","emitter.py"]

FROM base as collector

CMD ["python", "-u", "collector.py"]
