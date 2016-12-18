# encoding: utf-8

from urllib.request import urlopen, Request
from lxml import etree
from io import BytesIO
from kafka_header import *
import time

URI = 'http://airsoft-rus.ru'

get_page_url = lambda x, uri=URI: '{}/catalog/1020/?PAGEN_1={}'.format(uri, x)

html = urlopen(Request(get_page_url(1), headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})).read()
parser = etree.HTMLParser()
tree = etree.parse(BytesIO(html), parser)
pages_num = [i.text for i in tree.xpath('//*/nav[@class="paging"]/ul/li[*]/a')]
last_page = int(pages_num[-1])

for i in range(1, last_page + 1):
  html = urlopen(Request(get_page_url(i), headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})).read()

  tree = etree.parse(BytesIO(html), parser)

  items = tree.xpath('//*[@id="content"]/section/div/div[*]/div[*]/div[*]')

  for item in items:
    try:
      link = '{}{}'.format(URI, item[0][0][0].attrib['href'])
      title = item[0][1][0][0].text.strip()
      code = ' '.join(item[0][1][1][0].text.split(' ')[1:])
      made = ' '.join(item[0][1][1][1].text.split(' ')[1:])
      price = int(item[0][1][2][1].text.replace(' ', '').replace(u'р.', '').strip())
      photos = ['{}{}'.format(URI, item[0][0][0][0].attrib['src'])]

      product = {
        'link': link,
        'title': title,
        'made': made,
        'code': code,
        'price': price,
        'photos': photos,
        'store': 'airsoftrusru',
        'timestamp': int(time.time()),
        'active': True
      }

      future = producer.send(topic_prefix + 'default', product)

    except Exception as e:
      print(e)
