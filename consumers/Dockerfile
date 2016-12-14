FROM python:slim

ADD     requirements.txt    requirements.txt

ADD     consumer.py         consumer.py

RUN     apt-get update
RUN     apt-get install -y postgresql python-psycopg2 libpq-dev
RUN     pip3 install -r requirements.txt
RUN     apt-get clean
RUN     chmod +x consumer.py

ENTRYPOINT  ["./consumer.py"]
CMD []
