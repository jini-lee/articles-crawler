import csv
from datetime import timedelta, datetime
from dateutil import parser
from scrapy.spider import BaseSpider
from crawler.items import ArticleItem
from scrapy.http.request import Request


class MajorArticle(BaseSpider):
    name = 'major'
    collection_name = 'major'
    allowed_domains = ['news.naver.com']
    start_urls = []
    dt = datetime.now()
    main_url = 'https://news.naver.com/main/list.nhn'

    def __init__(self, from_date=dt, to_date=dt):
        try:
            self.from_date = parser.parse(from_date)
            self.to_date = parser.parse(to_date)
        except Exception as e:
            print(e+' Input date value error (20180503, Aug 28 2008 12:00AM)')

        def daterange():
            for n in range(int((self.from_date - self.to_date).days)+1):
                yield self.from_date + timedelta(n)

        def make_start_urls():
            try:
                with open("majorarticle.csv") as c_file:
                    reader = csv.DictReader(c_file)
                    for row in reader:
                        for d in daterange():
                            self.start_urls += [row['url']+'&date='+d]
            except IOError as err:
                print("File error:" + str(err))

    # nurl, press, title, date
    def parse(self, response):
        try:
            page_urls = response.xpath(
                '//div[@class="topbox_type6"]')[0].xpath(
                        'div/ul/li/a').css('a::attr(href)').extract()
            for purl in page_urls:
                yield Request(
                    self.main_url+purl,
                    callback=self.parse_article_page)
        except Exception as e:
            print(e)

    def parse_article_page(self, response):
        try:
            article_urls = response.xpath(
                '//ul[@class="type13 firstlist"]/li/dl/dt/a').css(
                    'a::attr(href)').extract()
            for aurl in article_urls:
                yield Request(aurl, callback=self.getUrl)
        except Exception as e:
            print(e)

    def getUrl(self, response):
        # Save item
        item = ArticleItem()
        item['nurl'] = response.url
        item['aid'] = item['nurl'][-10:]
        item['press'] = response.xpath(
            '//div[@class="press_logo"]/a/img/@title').extract()
        item['title'] = response.xpath(
            '//h3[@id="articleTitle"]/text()').extract()
        item['article_body'] = ''.join(response.xpath(
            '//div[@id="articleBodyContents"]/text()').extract()).strip()
        item['date'] = response.xpath(
            '//span[@class="t11"]/text()').extract()
        item['purl'] = response.xpath(
            '//div[@class="article_btns"]/a/@href').extract()
        item['nclass'] = response.xpath(
            '//div[@id="snb"]/h2/a/text()').extract()
        item['nclass2'] = response.xpath(
            '//ul[@class="nav"]/li[@class="on"]/a/text()').extract()
        return item
