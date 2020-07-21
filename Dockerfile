FROM python:3.8.3-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SQLALCHEMY_DATABASE_URI "sqlite://"

CMD [ "python", "-m", "openapi_server" ]
