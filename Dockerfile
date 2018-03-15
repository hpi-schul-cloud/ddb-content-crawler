FROM python:alpine

RUN mkdir -p /app/
WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD src/ /app/src/
ADD src/schema/ /app/src/schema/
ADD src/crawler/ /app/src/crawler/
ADD data/ /app/data/

WORKDIR /app/src
ENV PYTHONUNBUFFERED=1

ENTRYPOINT python -m app
