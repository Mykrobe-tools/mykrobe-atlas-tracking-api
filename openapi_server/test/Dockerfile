FROM python:3.8

COPY ../../ .

RUN pip install -r requirements.txt
RUN pip install -r test-requirements.txt

CMD pytest