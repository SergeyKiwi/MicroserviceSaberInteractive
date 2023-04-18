FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./builds /app/builds
COPY ./src /app/src

RUN pip install -r /app/requirements.txt


