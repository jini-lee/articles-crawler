import csv
import datetime
""" download pdf
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
"""

from scrapy.spider import BaseSpider
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.selector import Selector
from crawler.items import ArticleItem

from scrapy.http.request import Request


class AllArticleSpider(BaseSpider):
    name = 'all'
    collection_name = 'all'
    allowed_domains = ['news.naver.com']
    start_urls = []

    try:
        with open("allarticle.csv") as c_file:
            reader = csv.DictReader(c_file)
            for row in reader:
                start_urls += [row['url']]
    except IOError as err:
        print("File error:" + str(err))
   
   # nurl, press, title, date
    def parse(self, response):
        sel = Selector(response)
        nurl1s = sel.xpath('//ul[@class="type06_headline"]')
        nurl2s = sel.xpath('//ul[@class="type06"]')
        for nurl1 in nurl1s:
            url1 = nurl1.xpath('li/dl/dt[@class="photo"]/a/@href').extract()
            for u1 in url1:
                yield Request(u1, callback=self.getUrl)
        for nurl2 in nurl2s:
            url2 = nurl2.xpath('li/dl/dt[@class="photo"]/a/@href').extract()
            for u2 in url2:
                yield Request(u2, callback=self.getUrl)

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
        # item['body'] = response.xpath('//html').extract()
        # item['html'] = 'html/'
        # Save PDF
        """app = QApplication(sys.argv)
        web = QWebView()
        web.load(QUrl(item['nurl']))
        printer = QPrinter()
        printer.setPageSize(QPrinter.A4)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName("pdf/"+item['aid']+".pdf")

        def convertIt():
            web.print_(printer)
            QApplication.exit()

        QObject.connect(web, SIGNAL("loadFinished(bool)"), convertIt)
        app.exec_()
        """
        return item


class MajorArticle(BaseSpider):
    name = 'major'
    collection_name = 'major'
    allowed_domains = ['news.naver.com']
    start_urls = []
    dt = datetime.datetime.now()
    # date_param = dt.strftime("&date=%Y%m%d")
    date_param = '&date=20190111'
    main_url = 'https://news.naver.com/main/list.nhn'
    try:
        with open("majorarticle.csv") as c_file:
            reader = csv.DictReader(c_file)
            for row in reader:
                start_urls += [row['url']+date_param]
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
        # item['body'] = response.xpath('//html').extract()
        # item['html'] = 'html/'
        return item
