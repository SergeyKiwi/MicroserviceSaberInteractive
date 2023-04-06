FROM python:3.10-alpine

WORKDIR /app

ARG IP=0.0.0.0
ARG PORT="8000"

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./builds /app/builds
COPY ./src /app/src


