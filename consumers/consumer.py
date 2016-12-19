#!/usr/bin/env python3

from kafka import KafkaConsumer
from kafka.errors import KafkaError
import os, ssl
import json
import psycopg2
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def del_quote(s):
  return s.replace('"', '')

def prep_cert(cert):
  return del_quote(cert.replace('\\n', '\n')) + '\n'

ca = prep_cert(os.environ.get('CLOUDKARAFKA_CA'))
cert = prep_cert(os.environ.get('CLOUDKARAFKA_CERT'))
key = prep_cert(os.environ.get('CLOUDKARAFKA_PRIVATE_KEY'))

db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_host = os.environ.get('DB_HOST')
db_password = os.environ.get('DB_PASSWORD')

with open("/tmp/ca_cert.pem", "w") as f:
  f.write(ca)
with open("/tmp/signed_cert.pem", "w") as f:
  f.write(cert)
with open("/tmp/private_key.pem", "w") as f:
  f.write(key)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.check_hostname = True
ssl_context.load_verify_locations('/tmp/ca_cert.pem')
ssl_context.load_cert_chain('/tmp/signed_cert.pem', '/tmp/private_key.pem')

brokers = del_quote(os.environ.get('CLOUDKARAFKA_BROKERS')).split(',')
topic_prefix = del_quote(os.environ.get('CLOUDKARAFKA_TOPIC_PREFIX'))

consumer = KafkaConsumer(topic_prefix + 'default',
                         group_id='my-group',
                         bootstrap_servers=brokers,
                         security_protocol='SSL',
                         ssl_context=ssl_context,
                         api_version=(0, 9))

conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(db_name, db_user, db_host, db_password))
cur = conn.cursor()

success = 0
errors = 0

logging.info('Start consuming')
for message in consumer:
  try:
    logging.info('Try to read new message: {}'.format(message.value.decode('utf-8')))

    record = json.loads(message.value.decode('utf-8'))

    link = record['link']
    title = record['title']
    brand = record['brand'] or 'NULL'
    code = record['code'] or 'NULL'
    weight = record['weight'] or 'NULL'
    power = record['power'] or 'NULL'
    blowback = record['blowback'] or 'NULL'
    power_source = record['power_source'] or 'NULL'
    hopup = record['hopup'] or 'NULL'
    length = record['length'] or 'NULL'
    price = record['price'] or 'NULL'
    availability = record['availability']
    photo = record['photos'][0] if len(record['photos']) > 0 else 'NULL'
    store = record['store']
    timestamp = record['timestamp']

    sql_query = "INSERT INTO product (link, title, brand, code, weight, power, blowback, power_source, hopup, length, price, availability, photo, store, timestamp) \
                 VALUES ($${}$$, $${}$$, $${}$$, $${}$$, {}, {}, {}, {}, {}, {}, {}, {}, $${}$$, $${}$$, to_timestamp({})) \
                 ON CONFLICT (link) \
                 DO UPDATE SET title = $${}$$, price={}, availability={}, photo=$${}$$, store=$${}$$, timestamp=to_timestamp({}) \
                 WHERE product.link=$${}$$"\
      .format(link, title, brand, code, weight, power, blowback, power_source, hopup, length, price, availability, photo, store, timestamp,
              title, price, availability, photo, store, timestamp, link)

    cur.execute(sql_query)
    conn.commit()
    logging.info('Update record: {}, {}'.format(link, title))
    success += 1
  except Exception as e:
    conn.rollback()
    logging.error(e)
    errors += 1
