AS Service
==========


[![Codacy Badge](https://api.codacy.com/project/badge/Grade/db2d2bb3d6e34747baa24a6985c21b90)](https://www.codacy.com/app/karelov-maksim/as-service?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=maxbr/as-service&amp;utm_campaign=badger)
[![Build Status](https://travis-ci.org/maxbr/as-parser.svg?branch=master)](https://travis-ci.org/maxbr/as-parser) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/30b7a795b48840bcab2df43d05e6f0bb)](https://www.codacy.com/app/karelov-maksim/as-parser?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=maxbr/as-parser&amp;utm_campaign=Badge_Grade)

## Components
* Kafka 
* NodeJS app
* Varnish
* Postgres
* Data producers
* Data consumers

## Related links
* Github - https://github.com/maxbr/as-service
* Docker hub - https://hub.docker.com/r/maxbr/as-producer
* Jenkins - https://jenkins-maxbr.rhcloud.com
* Docker service dashboard - https://console.hyper.sh
* Kafka dashboard - https://api.cloudkarafka.com
* Travis CI - https://travis-ci.org/maxbr/as-parser

## Deploy server
### Compose file
```
version: '2'
services:
  web:
    image: maxbr/as-web:latest
    size: s1
    ports:
      - "5050:5050"
    environment:
      - CLOUDKARAFKA_CA=[VAL]
      - CLOUDKARAFKA_PRIVATE_KEY=[VAL]
      - CLOUDKARAFKA_CERT=[VAL]
      - CLOUDKARAFKA_TOPIC_PREFIX=[VAL]
      - CLOUDKARAFKA_BROKERS=[VAL]
      - DB_NAME=[VAL]
      - DB_USER=[VAL]
      - DB_HOST=[VAL]
      - DB_PASSWORD=[VAL]
  varnish:
    image: maxbr/as-varnish:latest
    fip: [VAL]
    size: s3
    links:
      - web:web
    depends_on:
      - web
    ports:
      - "80:6081"
    environment:
      - BACKEND_HOST_A=web
```

### Usage
``hyper compose up -p webui``
