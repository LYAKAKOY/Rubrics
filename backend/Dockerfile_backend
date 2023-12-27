FROM python:3.11-alpine3.18 AS builder

COPY poetry.lock pyproject.toml ./
RUN python -m pip install --no-cache-dir poetry poetry-plugin-export && \
    poetry export --without-hashes --without test -f requirements.txt -o requirements.txt

FROM python:3.11-alpine3.18

WORKDIR /backend

RUN apk add postgresql-client build-base postgresql-dev

COPY --from=builder requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .
