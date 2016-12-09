# encoding: utf-8

from urllib.request import urlopen, Request
from lxml import etree
from io import BytesIO
from kafka_header import *

URI = 'http://sharomet.ru'

get_page_url = lambda x, uri=URI: '{}/category/strajkbolnoe-oruzhie/?page={}'.format(uri, x)

html = urlopen(Request(get_page_url(1), headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})).read()
parser = etree.HTMLParser()
tree = etree.parse(BytesIO(html), parser)
pages_num = [i.text for i in tree.xpath('//*[@id="product-list"]/div/ul/li[*]/a')][:-1]
last_page = int(pages_num[-1])

for i in range(1, last_page + 1):
  html = urlopen(Request(get_page_url(i), headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})).read()
  tree = etree.parse(BytesIO(html), parser)

  items = tree.xpath('//*[@id="product-list"]/ul[@class="thumbs product-list"]/li[*]')

  for item in items:
    link = item[0].attrib['href']
    title = item[0].attrib['title']
    #        articul = item[0][1][1][0].text
    # producer = item[0][1][1][1].text
    price = item[1][0].text.replace(' ', '').split(',')[0]

    product = {
      'link': '{}{}'.format(URI, link),
      'title': title,
      'made': None,
      'code': None,
      'price': price,
      'photos': [],
      'store': 'sharometru',
      'timestamp': 0
    }

    future = producer.send(topic_prefix + 'default', product)
