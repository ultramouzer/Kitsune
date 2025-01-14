FROM python:3.8

RUN apt-get update \
    && apt-get install -y \
        libpq-dev \
        curl \
        libmagic1 \
    && pip3 install uwsgi

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

ENV LANG=C.UTF-8

CMD uwsgi --http=0.0.0.0:80 \
    --manage-script-name \
    --mount /=server:app \
    --processes %k \
    --threads 1 \
    --master \
    --listen 40000 \
    --disable-logging \
    --log-5xx \
    --enable-threads
