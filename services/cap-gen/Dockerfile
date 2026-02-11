FROM python:3.11-alpine

COPY cap-gen/pyproject.toml /pyproject.toml
COPY cap-gen/requirements/ /requirements/
COPY cap-gen/src/ /src/
COPY cap-gen/tests/ /tests/

RUN mkdir /feeds

# Install the rss library from local repository
COPY rss /rss
RUN pip install /rss \
    && pip install -r /requirements/dev.txt \
    && pip install -e .

WORKDIR /src
