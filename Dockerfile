FROM python:3.7-alpine

MAINTAINER Rémi Alvergnat <toilal.dev@gmail.com>

WORKDIR /root

COPY / /root/guessit/
WORKDIR /root/guessit/

RUN pip install -e .

ENTRYPOINT ["guessit"]

