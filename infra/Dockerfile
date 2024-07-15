FROM python:3.10-slim as builder

RUN apt-get update && apt-get install -y \
    python3-dev \
    curl

RUN pip install poetry==1.5.1

WORKDIR /app

COPY ../pyproject.toml poetry.lock ./

RUN poetry install


FROM python:3.10-slim

ENV POETRY_VIRTUALENVS_IN_PROJECT=false

RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl


COPY --from=builder /root/.cache/pypoetry/virtualenvs/ /root/.cache/pypoetry/virtualenvs/

RUN pip install poetry==1.5.1


WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY ../. .

RUN chmod +x infra/docker-entrypoint.sh
# ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
