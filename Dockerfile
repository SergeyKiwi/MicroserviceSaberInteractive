FROM python:3.10-alpine

WORKDIR /app/src

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./builds /app/builds
COPY ./src /app/src

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
