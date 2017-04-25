# Lesson03: 分页数据抓取
回顾一下前两课的内容：

- 简单实现了一个爬虫
- 抽取了相关的信息
- 使用了pipeline对数据进行处理
- 实现了子页面的抓取

到目前为止，离一个完整的爬虫还差一个常用的功能，那就是分页功能实现。

## 分页数据抽取
和人类翻页查看数据类似，程序也可以模拟点击下一页来实现下一页数据的抽取。下面看实现代码：

```python
    def parse(self, response):
        """抽取新闻列表信息"""
        # 特别注意li的class名字后面有一个空格，这是一个坑
        li_list = response.xpath("//ul[@class='pic-event-over']/li[@class='pic-pack-out ']/div[@class='pic-pack-inner']")

        for li in li_list:
            # 循环获取title，url，date等信息
            title = li.xpath("./h3/a/text()").extract()
            url = li.xpath("./h3/a/@href").extract()
            date = li.xpath(".//span[@class='timer fl']/text()").extract()

            # 注意：extract方法的返回值是一个列表，取第一个元素即可
            # yield是python中的生成器
            item = {
                'title': title[0],
                'url': url[0],
                'date': date[0]
            }

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
        # 在抽取详情信息的时候，将meta传了过来
        item = response.meta['item']
        desc = response.xpath("//div[@class='pic-content']/p//text()").extract()
        desc = "\n".join(desc)
        item['desc'] = desc  # 加入新闻详情
        yield item
```

这里关键就量布：

1. 获取下一页的url
2. 请求下一页的url

如此即可。


