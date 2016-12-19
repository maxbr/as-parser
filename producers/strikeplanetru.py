# encoding: utf-8

from urllib.request import urlopen, Request
from lxml import etree
from io import BytesIO
from kafka_header import *
import time
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

URL = 'http://strikeplanet.ru'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
REQUEST_HEADERS = {'User-Agent': USER_AGENT}

logging.info('Parser was launched against {}'.format(URL))

get_page_url = lambda x, uri=URL: '{}/catalog/straykbolnoe-oruzhie/?pager=36&PAGEN_1={}'.format(uri, x)

html = urlopen(Request(get_page_url(1), headers=REQUEST_HEADERS)).read()
parser = etree.HTMLParser()
tree = etree.parse(BytesIO(html), parser)
pages = tree.xpath('//*[@id="content"]/div/div[3]/div[3]/div[3]/div[3]/ul')
last_page = int(pages[0][-2][0][0].text.strip())

logging.info('Parser found {} catalog pages'.format(last_page))

counter = 0
errors = 0

def remove_redundant(name):
  return name.replace('Модель автомата', 'Автомат')\
    .replace('Модель пистолета', 'Пистолет')\
    .replace('Модель пулемета', 'Пулемет')\
    .replace('Модель винтовки', 'Винтовка')


for i in range(1, last_page + 1):
  logging.info('Open page {}'.format(i))

  html = urlopen(Request(get_page_url(i), headers=REQUEST_HEADERS)).read()
  tree = etree.parse(BytesIO(html), parser)
  items = tree.xpath('//*[@id="content"]/div/div[3]/div[3]/div[4]/div[*]')

  for item in items:
    try:
      item = item[0]

      link = '{}{}'.format(URL, item[3][0].attrib['href'])
      title = remove_redundant(item[3][0].text.strip())

      image = '{}{}'.format(URL, item[2][0][0].attrib['src'].split('?')[0])
      photos = [image]

      try:
        brand = item[4][1].text.split(': ')[1]
      except:
        brand = None

      try:
        code = item[4][0].text.split(': ')[1]
      except:
        code = None

      try:
        price = int(item[5][0][0][0].text.strip().replace(' ', ''))
      except:
        price = None

      if len(item[0]) == 1:
        availability = 'склад' in item[0][0].text
      else:
        availability = 'ет в наличии' not in item[0].text

      print(link, image, title, availability, brand, code, price)

      timestamp = int(time.time())

      product = {
        'link': link,
        'title': title,
        'brand': brand,
        'code': code,
        'weight': None,
        'power': None,
        'blowback': None,
        'power_source': None,
        'hopup': None,
        'length': None,
        'price': price,
        'availability': availability,
        'photos': photos,
        'store': URL,
        'timestamp': timestamp
      }

      logging.info('Found: {}, {}, {}, {}'.format(link, title, price, timestamp))
      counter += 1
      future = producer.send(topic_prefix + 'default', product)

    except Exception as e:
      errors += 1
      logging.error(e)

logging.info('Total success: {}'.format(counter))
logging.info('Total failed: {}'.format(errors))
