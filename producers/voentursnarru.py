# encoding: utf-8

from urllib.request import urlopen, Request
from lxml import etree
from io import BytesIO
from kafka_header import *
import time
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

URL = 'http://voentursnar.ru'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
REQUEST_HEADERS = {'User-Agent': USER_AGENT}

logging.info('Parser was launched against {}'.format(URL))

parser = etree.HTMLParser()

html = urlopen(Request('{}/catalog/40/?limit=900'.format(URL), headers=REQUEST_HEADERS)).read()
tree = etree.parse(BytesIO(html), parser)
items = tree.xpath('//*[@class="offer_item"]')

def remove_redundant_words(name):
  return name.replace('ЭЛЕКТРОПНЕВМ.', '')\
    .replace('электропневм.', '')\
    .replace('пневм.', '')\
    .replace('ПНЕВМ.', '')\
    .replace('ПУЛЕМЁТ', 'Пулемет')\
    .replace('ПИСТОЛЕТ', 'Пистолет')\
    .replace('ВИНТОВКА', 'Винтовка')\
    .replace('Страйкбольный', '')\
    .replace('страйкбольный', '')\
    .replace('СТРАЙКБОЛЬНОЙ', '')\
    .replace('СТРАЙКБОЛЬНАЯ', '')\
    .replace('страйкбольная', '')\
    .replace('газов.', '')\
    .replace('КОРПУС В СБОРЕ', 'Корпус в сборе')\
    .replace('АВТОМАТ', 'Автомат').replace('  ', ' ')

counter = 0
errors = 0

for item in items:
  try:
    image = '{}{}'.format(URL, item[1][0][0].attrib['src'])
    link = '{}{}'.format(URL, item[2][0].attrib['href'])
    title = remove_redundant_words(item[2][0].text.strip())
    photos = [image]

    brand = None
    if title[-1] == ')' and '(' in title:
      brand = title[title.rindex('(')+1:-1]
    code = None

    try:
      price = int(str(etree.tostring(item[3][1][0])).split('</span>')[1].strip().replace('\\n', '').replace('\\t', '').replace('&#1088;&#1091;&#1073;\'', '').replace(' ', ''))
      if price == 0:
        price = None
    except:
      price = None

    availability = 'нет' not in item[4].text.strip()
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
