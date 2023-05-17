FROM python:3.10.11-slim-buster


COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src
COPY tests/ /tests/

WORKDIR /src
ENV FLASK_APP=rss/api/app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
