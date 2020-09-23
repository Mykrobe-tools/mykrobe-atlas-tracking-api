FROM python:3.8.3-slim-buster as compile-image

RUN apt update
RUN apt install -y --no-install-recommends libpq-dev build-essential

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.8.3-slim-buster
COPY --from=compile-image /opt/venv /opt/venv

COPY . .

ENV PATH="/opt/venv/bin:$PATH"
ENV SQLALCHEMY_DATABASE_URI "postgresql://postgres@localhost:5432"

CMD [ "python", "-m", "openapi_server" ]
