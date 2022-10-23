FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED 1

COPY . .

WORKDIR /barproject

EXPOSE 8000

RUN pip install --upgrade pip && \
    pip install -r ../requirements.txt
