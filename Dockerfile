# Global ARG, available to all stages (if renewed)
ARG WORKDIR="/app"

FROM python:3.11.9 AS builder

ARG WORKDIR

# Don't buffer `stdout`
ENV PYTHONUNBUFFERED=1
# Don't create `.pyc` files
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR ${WORKDIR}

RUN adduser --disabled-password --gecos '' python

COPY --chown=python:python pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --only main

FROM gcr.io/distroless/python3-debian12:nonroot AS runtime

ARG WORKDIR

WORKDIR ${WORKDIR}

COPY --from=builder /usr/lib/ /usr/lib/

COPY --from=builder ${WORKDIR}/.venv /usr/local

ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages:${PYTHONPATH}

COPY app ./app

EXPOSE 8000

ENTRYPOINT ["python", "app"]