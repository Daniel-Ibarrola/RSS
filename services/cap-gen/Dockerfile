FROM python:3.11-alpine

COPY pyproject.toml /pyproject.toml
COPY requirements/ /requirements/
COPY src/ /src/
COPY tests/ /tests/

# Git is necessary to install the rss dependency
RUN mkdir /feeds
RUN apk add --no-cache git

# TODO: can we find another way to install the rss module without git?
RUN pip install "git+https://github.com/Daniel-Ibarrola/RSS.git#subdirectory=services/rss" \
    && pip install -r /requirements/dev.txt \
    && pip install -e .

WORKDIR /src
