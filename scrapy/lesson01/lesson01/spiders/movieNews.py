# -*- coding: utf-8 -*-
import scrapy


class MovienewsSpider(scrapy.Spider):
    name = "movieNews"
    allowed_domains = ["www.1905.com"]
    start_urls = ['http://www.1905.com/list-p-catid-220.html']

    def parse(self, response):
        li_list = response.xpath("//ul[@class='pic-event-over']/li[@class='pic-pack-out']")
        #li_list = response.xpath("ul[@class='pic-event-over']/div[@class='pic-pack-inner']")
        print(li_list)

        data = []
        for li in li_list:
            title = li.xpath("./h3/a/text()").extract()
            url = li.xpath("./h3/a/@href").extract()
            date = li.xpath(".//span[@class='timer fl']/text()").extract()
            data.append({
                'title': title,
                'url': url,
                'date': date
            })

        print(data)
