FROM python:3.8

RUN apt update
RUN apt install -y --no-install-recommends postgresql

RUN