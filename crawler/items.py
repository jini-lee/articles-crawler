# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field
  
class ArticleItem(Item):
    title = Field()
    article_body = Field()
    date = Field()
    press = Field()
    purl = Field()
    nurl = Field()
    aid = Field()
    html = Field()
    ncomment = Field()
    nclass = Field()
    pclass = Field()
    nclass2 = Field()
    pclass2 = Field()
    pass
