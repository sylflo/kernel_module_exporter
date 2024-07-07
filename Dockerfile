FROM python:3.12-slim

RUN pip install --no-cache-dir poetry==1.8.3
RUN apt-get update --no-install-recommends && \
    apt-get --no-install-recommends install -y kmod=30+20221128-1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .

COPY ./docker/entrypoint.sh ./

ENTRYPOINT ["/app/entrypoint.sh"]
