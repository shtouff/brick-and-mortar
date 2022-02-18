# base, do not publish
FROM python:3.10.1-slim as base

WORKDIR /app

ENV PATH=/root/.local/bin:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN \
    useradd -m bam \
    && apt-get update -y \
    && apt-get install -y \
        curl \
        libffi7 \
        libmcrypt4 \
        libpq5 \
        tzdata \
        zlib1g \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false


# builder, do not publish
FROM base AS builder

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN \
    apt-get install -y \
        build-essential \
        libffi-dev \
        libmcrypt-dev \
        libpq-dev \
        zlib1g-dev \
    && poetry install --no-root --no-dev


# bam-base, do not publish
FROM base AS bam-base

WORKDIR /app

COPY --from=builder /usr/local/ /usr/local/
COPY --from=builder /app/ /app/


# bam, suitable for prod
FROM bam-base AS bam

WORKDIR /app

COPY . /app/

RUN poetry install --no-dev

# API
EXPOSE 5000

# finally set the user to non-root
USER bam

CMD ["flask", "run", "-h", "0.0.0.0"]


# bam-dev, suitable for unit testing
FROM bam-base AS bam-dev

WORKDIR /app

COPY . /app/

RUN poetry install

USER root

CMD ["pytest"]