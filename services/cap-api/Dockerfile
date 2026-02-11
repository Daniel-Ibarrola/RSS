FROM python:3.11-alpine

COPY cap-api/pyproject.toml /pyproject.toml
COPY cap-api/requirements/ /requirements/
COPY cap-api/src/ /src/
COPY cap-api/tests/ /tests/

# Install curl to perform health checks
RUN apk add --no-cache curl

# Install the rss library from local repository
COPY rss /rss
RUN pip install /rss \
    && pip install -r /requirements/dev.txt \
    && pip install -e .

WORKDIR /src
