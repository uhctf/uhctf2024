FROM python:3.8-slim-buster

WORKDIR /app
COPY ./src /app

RUN pip3 install -r ./requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]