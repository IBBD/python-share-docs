# Lesson08: scrapy爬虫程序的调试
爬虫在执行的过程中可能会出现各种问题，怎么调试往往是非常重要的。下面会介绍几种调试的方式：

## Scrapy Shell
爬虫最常见的问题是，抓取不到数据，这时很可能就是selector（例如xpath）写得不对。而scrapy shell就是调试这种问题的利器。

进入shell的两种方式：

- 第一种方式：直接进入shell：

```sh
scrapy shell 'https://docs.scrapy.org/en/latest/topics/debug.html'
```

这时就会进入一下控制台，可以理解为到了爬虫的parse部分，正常情况下网页数据已经下载回来了，response对象已经生成，在控制台中都可以直接使用。

- 第一种方式：在爬虫中进入shell：

第一种方式虽然简单，但是有麻烦的地方，例如shell的执行环境和爬虫的执行环境可能不一致，因为爬虫可能使用了user-agent等，这时使用第一种方式就不是那么合适。另外，如果是希望爬虫在满足某些条件的情况下才调用shell，这时第一种方式也是实现不了的。

代码实现大致如下：

```python
from scrapy.shell import inspect_response

class MovienewsSpider(scrapy.Spider):

    def parse(self, response):
        # do somethings...

        # 进入debug命令行
        # 这里可以加if判断，例如：if len(li_list) == 0
        # 这时才调用shell进行测试调试
        inspect_response(response, self)

        # do more ...
```




