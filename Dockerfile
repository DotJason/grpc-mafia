FROM python:3.10

COPY client/ client/
COPY server/ server/
COPY proto/ proto/
COPY lib/ lib/
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENV PYTHONPATH .

WORKDIR .
