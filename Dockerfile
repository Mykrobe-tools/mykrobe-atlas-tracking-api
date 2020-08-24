FROM python:3.8.3-slim-buster

RUN apt update
RUN apt install -y --no-install-recommends libpq-dev build-essential

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SQLALCHEMY_DATABASE_URI "postgresql://postgres@localhost:5432"

CMD [ "python", "-m", "openapi_server" ]
