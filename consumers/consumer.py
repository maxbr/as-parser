#!/usr/bin/env python3

from kafka import KafkaConsumer
from kafka.errors import KafkaError
import os, ssl
import json
import psycopg2

#
# run locally: set -o allexport && source ../env2 && python3 consumer.py
#

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

print('Start consuming')
for message in consumer:
  try:
    record = json.loads(message.value.decode('utf-8'))

    print(record['title'])
    cur.execute("INSERT INTO product (link, title, made, code, price, photo, store, timestamp, active) VALUES "
                "($${}$$, $${}$$, $${}$$, $${}$$, {}, $${}$$, $${}$$, {}, {})".format(record['link'], record['title'],
                                                                          record['made'], record['code'],
                                                                          record['price'], record['photos'][0],
                                                                          record['store'], record['timestamp'],
                                                                          record['active']))
    conn.commit()
  except Exception as e:
    print(e)
