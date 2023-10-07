FROM python:3.9-slim-buster

WORKDIR /get_a_pic_app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /get_a_pic_app/