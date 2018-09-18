FROM python:3.6.6-alpine AS builder
MAINTAINER Vitor Mantovani <vtrmantovani@gmail.com>

RUN apk add --no-cache --update bash git py-mysqldb gcc libxslt-dev openssh mariadb-dev libffi-dev linux-headers alpine-sdk

RUN addgroup ibm && adduser -D -h /home/ibm -G ibm ibm

USER ibm
RUN mkdir /home/ibm/pxa
RUN mkdir /home/ibm/logs
ADD wsgi.py /home/ibm/
ADD requirements.txt /home/ibm/
ADD pxa /home/ibm/pxa
ADD manager.py /home/ibm/

RUN cd /home/ibm && rm -rf /home/ibm/.venv && /usr/local/bin/python -m venv .venv \
    && /home/ibm/.venv/bin/pip install --upgrade pip
RUN cd /home/ibm && /home/ibm/.venv/bin/pip install -r requirements.txt

FROM python:3.6.6-alpine

RUN apk add --no-cache --update bash git py-mysqldb gcc libxslt-dev openssh mariadb-dev libffi-dev linux-headers alpine-sdk

COPY --from=builder /home/ibm /home/ibm

RUN addgroup ibm && adduser -D -h /home/ibm -G ibm ibm

USER root
RUN chown ibm.ibm /home/ibm -R

USER ibm
ADD ./dockerfiles/uwsgi.ini /home/ibm/

ADD ./dockerfiles/newrelic.ini /home/ibm/
ENV NEW_RELIC_CONFIG_FILE=/home/ibm/newrelic.ini

EXPOSE 8080
CMD ["/home/ibm/.venv/bin/newrelic-admin", "run-program", "/home/ibm/.venv/bin/uwsgi", "--ini", "/home/ibm/uwsgi.ini"]