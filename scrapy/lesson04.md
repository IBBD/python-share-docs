# Lesson04: 配置文件及反爬虫机制应对
回顾一下前面部分的课程内容：

- 简单实现了一个爬虫
- 抽取了相关的信息
- 使用了pipeline对数据进行处理
- 实现了子页面的抓取
- 分页数据抓取
- 数据存储到csv文件

本节课程目标：

- 配置文件解释
- 中间件实现
- 爬虫参数配置

有了配置文件和user agent中间件的实现，基本就能应付大多数网站的反爬虫机制了。

## 配置文件解释
配置文件主要是指`settings.py`，在前面的课程中也略有涉及，主要是pipeline的配置。一些比较重要的配置：

- 下载延迟：`DOWNLOAD_DELAY = 3`该参数可以控制抓取的频率，可以避免抓取过快而导致被封。
- 下载中间件配置
- 爬虫中间件
- cookie设置：可以用于模拟登陆

具体的配置可以看配置文件即可。

## 中间件实现
随着项目生成默认就会生成一个spider middleware的样例文件，可以在`settings.py`中开启：

```python
SPIDER_MIDDLEWARES = {
    'lesson01.middlewares.Lesson01SpiderMiddleware': 543,
}
```

修改其代码如下：

```python
class Lesson01SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.
        print("*"*30, "process_spider_input")

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
        print("*"*30, "process_spider_output")

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.
        print("*"*30, "process_spider_exception")

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.
        print("*"*30, "process_start_requests")

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        print("*"*30, "spider_opened")
        spider.logger.info('Spider opened: %s' % spider.name)
```

其中`print`是为了方便观察其调用顺序而输出的（注意：在scrapy1.3.3版本生成的代码中，方法里少了一个`self`！）。经观察，其顺序如下：

1. spider_opened
2. process_start_requests
3. process_spider_input
4. process_spider_output
5. parse: 这里才到对页面数据的抽取

这相当于为爬虫提供了多个注入点，可以用于做统计，调度等操作。

另外比较常用的中间件，还有用于设置User-agent的，使爬虫看起来更像人类操作。代码例如：

```python
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random


class UserAgent(UserAgentMiddleware):

    user_agent_pool = [
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
        # more ......
    ]

    def __init(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_pool)
        if ua:
            request.headers.setdefault('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
            request.headers.setdefault('Accept-Encoding', 'gzip, deflate, sdch')
            request.headers.setdefault('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
            request.headers.setdefault('User-Agent', ua)

        if 'headers' in request.meta:
            # 设置头信息
            for header in request.meta['headers']:
                request.headers.setdefault(header['key'], header['value'])
```

因为中间件可能会有多个，所以我们建立一下独立的`middlewares`文件夹，将相关的中间件都统一到该目录下，方便管理。

user agent的中间件也是需要在settings.py中配置启用的：

```python
DOWNLOADER_MIDDLEWARES = {
    #'lesson01.middlewares.MyCustomDownloaderMiddleware': 543,
    'lesson01.middlewares.user_agent.UserAgent': 400,
}
```

## 爬虫参数配置
有时候，我们运行爬虫的时候，需要动态得设置一些参数。参数我们也可以设置在`settings.py`的配置文件中，但是那样子每次运行的时候，都需要修改代码才能执行。这时通过动态参数运行时设置参数最好。

文档见：https://docs.scrapy.org/en/latest/intro/tutorial.html#using-spider-arguments

例如，原来我们需要抓取的列表入口地址为`http://www.1905.com/list-p-catid-220.html`，这是指定的，其中`catid`的值为220，这是其中一个分类id，但是在很多情况下，看你是有很多分类的，这时就需要通过参数来配置抓取不同的类别了。爬虫代码实现如下：

```python
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
        # more...（后面的省略）
```

这时，运行爬虫的时候就可以使用下面的命令：

`scrapy crawl movieNews -a catid=220`

其中`-a`就是增加参数，`catid`就是参数名，`220`就是参数值。可以使用多个参数，例如这样：`scrapy crawl spiderName -a paramName1=value1 -a paramName2=value2 -a paramName3=value3`

这是参数的一种使用场景，参数还可以用于其他的场景，例如`-a debug=True`就可以通过debug参数来判断是否是测试状态了。

