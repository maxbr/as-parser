AS Service
==========

[![Build Status](https://travis-ci.org/maxbr/as-parser.svg?branch=master)](https://travis-ci.org/maxbr/as-parser) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/db2d2bb3d6e34747baa24a6985c21b90)](https://www.codacy.com/app/karelov-maksim/as-service?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=maxbr/as-service&amp;utm_campaign=Badge_Grade)

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
* Travis CI - https://travis-ci.org/maxbr/as-service

## Deploy

**dev:** ``docker-compose -f docker-compose.yml -f dev.yml up -d -p project``

**hyper:** ``hyper compose up -f docker-compose.yml -f prod.yml -d -p project``
