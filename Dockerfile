FROM python:3.10-slim AS builder
WORKDIR /app
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

RUN pip3 install -U poetry

COPY /tele_plan /app/tele_plan
COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-dev

ENTRYPOINT ["poetry","run","python3","/app/tele_plan/tele_plan.py"]