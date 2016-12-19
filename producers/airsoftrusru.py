# encoding: utf-8

from urllib.request import urlopen, Request
from lxml import etree
from io import BytesIO
from kafka_header import *
import time
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

URL = 'http://airsoft-rus.ru'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
REQUEST_HEADERS = {'User-Agent': USER_AGENT}

logging.info('Parser was launched against {}'.format(URL))

get_page_url = lambda x, uri=URL: '{}/catalog/1020/?page_count=100&PAGEN_1={}'.format(uri, x)

html = urlopen(Request(get_page_url(1), headers=REQUEST_HEADERS)).read()
parser = etree.HTMLParser()
tree = etree.parse(BytesIO(html), parser)
pages_num = [i.text for i in tree.xpath('//*/nav[@class="paging"]/ul/li[*]/a')]
last_page = int(pages_num[-1])

logging.info('Parser found {} catalog pages'.format(len(pages_num)+1))

counter = 0
errors = 0

for i in range(1, last_page + 1):
  logging.info('Open page {}'.format(i))

  html = urlopen(Request(get_page_url(i), headers=REQUEST_HEADERS)).read()
  tree = etree.parse(BytesIO(html), parser)
  items = tree.xpath('//*[@id="content"]/section/div/div[*]/div[*]/div[*]')

  for item in items:
    try:
      link = '{}{}'.format(URL, item[0][0][0].attrib['href'])
      title = item[0][1][0][0].text.strip()

      image = item[0][0][0][0].attrib['src'] if len(item[0][0][0]) == 1 else item[0][0][0][1].attrib['src']
      photos = ['{}{}'.format(URL, image)]

      try:
        code = ' '.join(item[0][1][1][0].text.split(' ')[1:])
      except:
        code = None

      try:
        brand = ' '.join(item[0][1][1][1].text.split(' ')[1:])
      except:
        brand = None

      price_holder = item[0][1][2]
      if len(price_holder) == 3:
        price = int(price_holder[2].text.replace(' ', '').replace(u'р.', '').strip())
      elif len(price_holder) == 0:
        price = None
      else:
        price = int(price_holder[1].text.replace(' ', '').replace(u'р.', '').strip())

      availability = 'недоступен' not in item[0][2].text

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
