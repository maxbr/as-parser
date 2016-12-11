FROM python:slim

ADD     requirements.txt    requirements.txt

ADD     kafka_header.py     kafka_header.py
ADD     run_consumer.py     run_consumer.py

ADD     airsoftrusru.py     airsoftrusru.py
ADD     sharometru.py       sharometru.py
ADD     voentursnarru.py    voentursnarru.py

RUN     apt-get update && apt-get install -y gcc libxml2-dev libxslt1-dev libz-dev
RUN     pip3 install -r requirements.txt
RUN     apt-get remove -y gcc && apt-get clean
RUN     echo '#!/bin/sh\npython3 $@' > entrypoint.sh
RUN     chmod +x entrypoint.sh

ENTRYPOINT  ["./entrypoint.sh"]
CMD []
