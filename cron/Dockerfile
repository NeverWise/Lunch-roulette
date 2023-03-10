FROM python:3.11-alpine3.17
LABEL maintainer="Matteo Pomi"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    echo "* * * * * python /app/random-event.py" >> /etc/crontabs/root

ENV PATH="/py/bin:$PATH"
