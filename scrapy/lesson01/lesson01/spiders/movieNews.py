# -*- coding: utf-8 -*-
import scrapy
from lesson01.items import Article
from scrapy.exceptions import CloseSpider


class MovienewsSpider(scrapy.Spider):
    name = "movieNews"
    allowed_domains = ["www.1905.com"]
    start_urls = ['http://www.1905.com/list-p-catid-%s.html']

    def start_requests(self):
        # catid = 220
        catid = getattr(self, 'catid', None)
        if catid is None:
            raise CloseSpider("catid param is not set")

        for url in self.start_urls:
            url = url % catid
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        """抽取新闻列表信息"""
        print("*"*30, "parse")

        # 特别注意li的class名字后面有一个空格，这是一个坑
        li_list = response.xpath("//ul[@class='pic-event-over']/li[contains(@class, 'pic-pack-out')]/div[@class='pic-pack-inner']")

        for li in li_list:
            # 循环获取title，url，date等信息
            title = li.xpath("./h3/a/text()").extract()
            url = li.xpath("./h3/a/@href").extract()
            date = li.xpath(".//span[@class='timer fl']/text()").extract()

            # 注意：extract方法的返回值是一个列表，取第一个元素即可
            # yield是python中的生成器
            item = Article(title=title[0], url=url[0], date=date[0])

            # meta参数可以将已经获取的item数据传给详情解释函数
            # callback参数指定详情页面的解释函数
            yield scrapy.Request(url[0],
                                 meta={'item': item},
                                 callback=self.parse_desc)

        # 获取列表下一页的链接
        next_page = response.xpath("//div[@id='paging']/a[@class='next']/@href").extract()

        # 下一页是和第一页相同的列表页，所以callback也是parse
        yield scrapy.Request(next_page[0],
                             callback=self.parse)

    def parse_desc(self, response):
        """抽取详情"""
        print("*"*30, "parse_desc")

        # 在抽取详情信息的时候，将meta传了过来
        item = response.meta['item']
        desc = response.xpath("//div[@class='pic-content']/p//text()").extract()
        desc = "\n".join(desc)
        item['desc'] = desc  # 加入新闻详情
        # raise CloseSpider("==")

        yield item
