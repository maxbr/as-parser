FROM python:slim

ADD     requirements.txt    requirements.txt

ADD     kafka_header.py     kafka_header.py
ADD     run_consumer.py     run_consumer.py

ADD     airsoftrusru.py     airsoftrusru.py
ADD     sharometru.py       sharometru.py
ADD     voentursnarru.py    voentursnarru.py

RUN     pip3 install -r requirements.txt
RUN     echo '#!/bin/sh\npython3 $@' > entrypoint.sh
RUN     chmod +x entrypoint.sh

ENTRYPOINT  ["./entrypoint.sh"]
CMD []
