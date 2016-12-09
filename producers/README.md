Producers and Docker image
==========================

## Producers

**Scripts produce data to kafka brokers in the following format:**

```
{
    "link": "full-link-to-item",
    "title": "product-title",
    "made": "made-by-company",
    "code": "product-code",
    "price": price-in-rubles,
    "photos": ["image-link-1", "image-link-2"],
    "store": "scriptname",
    "timestamp": timestamp-when-parsed
}
```

## Usage
For container run you need to pass the following environment variables:
  
  * ``CLOUDKARAFKA_CA``
  * ``CLOUDKARAFKA_CERT``
  * ``CLOUDKARAFKA_PRIVATE_KEY``
  * ``CLOUDKARAFKA_TOPIC_PREFIX``
  * ``CLOUDKARAFKA_BROKERS``

**to build image:**
``docker build -t maxbr/as-parser:latest producers``

**to run locally:**
``docker run --rm --env-file=env maxbr/as-parser:latest [SCRIPT_FILE]``

**to run by hyper:**
``hyper run --size=s3 --rm --env-file=env maxbr/as-parser:latest [SCRIPT_FILE]``

**to check that kafka brokers get data run consumer:**
``docker run --rm --env-file=env maxbr/as-parser:latest run_consumer.py``

## Supported stores

| name        |      link              |  script         |
|-------------|:----------------------:|:---------------:|
| airsoft rus | http://airsoft-rus.ru  | airsoftrusru.py |
| sharomet    | http://sharomet.ru     | sharometru.py   |
| voentursnar | http://voentursnar.ru  | voentursnar.py  |

backlog: *airsoftbox.ru, strikeplanet.ru, airsoftstore.ru, air-wars.ru, kalibr603.ru, 6mm.ru, kugel.ru*

## Related links

  * [maxbr/as-parser image on Docker Hub](https://hub.docker.com/r/maxbr/as-parser)
  * [maxbr/as-parser build page on Travis CI](https://travis-ci.org/maxbr/as-parser)
  