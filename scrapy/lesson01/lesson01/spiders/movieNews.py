# -*- coding: utf-8 -*-
import scrapy


class MovienewsSpider(scrapy.Spider):
    name = "movieNews"
    allowed_domains = ["www.1905.com"]
    start_urls = ['http://www.1905.com/list-p-catid-220.html']

    def parse(self, response):
        # 特别注意li的class名字后面有一个空格，这是一个坑
        li_list = response.xpath("//ul[@class='pic-event-over']/li[contains(@class, 'pic-pack-out')]/div[@class='pic-pack-inner']")

        data = []
        count = 0
        for li in li_list:
            # 循环获取title，url，date等信息
            title = li.xpath("./h3/a/text()").extract()
            url = li.xpath("./h3/a/@href").extract()
            date = li.xpath(".//span[@class='timer fl']/text()").extract()
            # 注意：extract方法的返回值是一个列表，取第一个元素即可
            data.append({
                'title': title[0],
                'url': url[0],
                'date': date[0]
            })

            count += 1
            print("*"*10, count, "*"*10)

        print(data)
