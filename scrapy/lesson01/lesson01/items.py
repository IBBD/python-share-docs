# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Lesson01Item(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()  # 新闻标题
    url = scrapy.Field()    # 新闻链接
    date = scrapy.Field()   # 新闻发布日期
    desc = scrapy.Field()   # 新闻详情
