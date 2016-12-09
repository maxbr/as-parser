from kafka import KafkaConsumer
from kafka.errors import KafkaError
import os, ssl
import json

def del_quote(s):
  return s.replace('"', '')

def prep_cert(cert):
  return del_quote(cert.replace('\\n', '\n')) + '\n'

ca = prep_cert(os.environ.get('CLOUDKARAFKA_CA'))
cert = prep_cert(os.environ.get('CLOUDKARAFKA_CERT'))
key = prep_cert(os.environ.get('CLOUDKARAFKA_PRIVATE_KEY'))

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
print ('Start consuming')
for message in consumer:
    # print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
    print(json.loads(message.value.decode('utf-8')))
