import urllib2
from lxml import etree
from StringIO import StringIO


html = urllib2.urlopen('http://voentursnar.ru/catalog/40/?limit=12&arrFilter_14=1506745864&arrFilter_P1_MIN=&arrFilter_P1_MAX=&set_filter=%CF%EE%EA%E0%E7%E0%F2%FC&PAGEN_1=1').read()
parser = etree.HTMLParser()
tree = etree.parse(StringIO(html), parser)

pages_num = [x[0].text for x in tree.xpath('/html/body/div[2]/div[4]/div[2]/div[4]/div[13]/div/div/ul/li[*]')][:-1]
last_page = int(pages_num[-1])

catalog = []

for i in range(1, last_page+1):
    html = html = urllib2.urlopen('http://voentursnar.ru/catalog/40/?limit=12&arrFilter_14=1506745864&arrFilter_P1_MIN=&arrFilter_P1_MAX=&set_filter=%CF%EE%EA%E0%E7%E0%F2%FC&PAGEN_1=1').read()
    tree = etree.parse(StringIO(html), parser)
    items = tree.xpath('//*[@class="offer_item"]')

    for item in items:
        link = item[2][0].attrib['href']
        title = item[2][0].text
        price = item[3][0].text.strip()

        catalog.append((link, title, price))
    

