# Lesson02: 爬虫的数据处理及存储
回顾一下Lesson01的内容：

- 简单实现了一个爬虫
- 抽取了相关的信息

但是抽取的数据只是做了简单的print，这其实是比较难应用的。Lesson02的两个目标：

1. 将要对数据处理进行完善;
2. 实现子页面的抓取。

## Scrapy爬虫的流程及架构
下图显示了Scrapy的大体架构，其中包含了它的主要组件及系统的数据处理流程（绿色箭头所示）。下面就来一个个解释每个组件的作用及数据的处理过程。

![Scrapy架构图](/scrapy/_images/scrapy_architecture.png)

## 完善数据处理流程

- 1. 定义items

在lesson01的第1个创建项目的步骤中，提到目录结构，里面有一个`items.py`的文件，其默认内容如下：

```python
import scrapy

class Lesson01Item(scrapy.Item):
    pass
```

这里，我们定义我们爬虫会爬取的数据，如下：

```python
import scrapy

class Lesson01Item(scrapy.Item):
    title = scrapy.Field()  # 新闻标题
    url = scrapy.Field()    # 新闻链接
    date = scrapy.Field()   # 新闻发布日期
    desc = scrapy.Field()   # 新闻详情
```

这样我们就定义好了我们需要的数据。

- 2. 在pipeline中处理数据

同样在lesson01提到的目录结构中，有一个`pipelines.py`的文件，在这里我们可以很方便的对数据进行处理，如下：

```python
class Lesson01Pipeline(object):
    def process_item(self, item, spider):
        # 处理数据通常是存储到数据库，如mysql，mongodb, csv等
        # 为了演示方便，这里只是简单的print
        print(item)

        return item
```

- 3. 将数据传到pipeline

要传数据到pipeline中也是比较简单，只需要修改一下我们的movieNews爬虫即可：

```python
import scrapy

class MovienewsSpider(scrapy.Spider):
    name = "movieNews"
    allowed_domains = ["www.1905.com"]
    start_urls = ['http://www.1905.com/list-p-catid-220.html']

    def parse(self, response):
        # 特别注意li的class名字后面有一个空格，这是一个坑
        li_list = response.xpath("//ul[@class='pic-event-over']/li[@class='pic-pack-out ']/div[@class='pic-pack-inner']")

        for li in li_list:
            # 循环获取title，url，date等信息
            title = li.xpath("./h3/a/text()").extract()
            url = li.xpath("./h3/a/@href").extract()
            date = li.xpath(".//span[@class='timer fl']/text()").extract()

            # 注意：extract方法的返回值是一个列表，取第一个元素即可
            # yield是python中的生成器
            yield {
                'title': title[0],
                'url': url[0],
                'date': date[0]
            }
```

关于生成器 yield，简单地讲，yield 的作用就是把一个函数变成一个 generator，带有 yield 的函数不再是一个普通函数，Python 解释器会将其视为一个 generator。

注意：yield返回的对象，里面的title, url, date等元素都是已经定义好了在items.py文件中的。

- 4. 修改配置文件settings.py

到目前为止，如果我们直接运行爬虫的话，就会发现，我们定义的pipeline好像完全没有效果，这是因为在settings.py中，默认并没有开启pipeline。默认配置如下：

```python
#ITEM_PIPELINES = {
#    'lesson01.pipelines.Lesson01Pipeline': 300,
#}
```

将前面的＃号去掉即可，其中Lesson01Pipeline就是pipeline中的类名。

到这里，我们就可以运行爬虫看结果了，还是命令`scrapy crawl movieNews`，从结果中，就会看到相应的输出：

```
{'date': '2017-04-24', 'title': '再现真实历史 史诗电影《血战湘江》河北巡回展...', 'url': 'http://www.1905.com/news/20170424/1177156.shtml'}
{'date': '2017-04-24', 'title': '万达原力北影节联手 打造国产3D动画《妈妈咪鸭...', 'url': 'http://www.1905.com/news/20170424/1177145.shtml'}
{'date': '2017-04-24', 'title': '品质良莠不齐超半数难回本 网络电影路在何方？', 'url': 'http://www.1905.com/news/20170424/1177124.shtml'}
...
```

## 实现子页面的抓取
新闻类页面的特点是：新闻详情的页面通常不在新闻的列表页面上，如果需要抓取到详情内容，必须实现子页面的抓取。

我们打开其中一个详情页面，例如`http://www.1905.com/news/20170424/1177078.shtml`，首先要做的就是理解其页面结构：

![详情页的页面结构](/scrapy/_images/scrapy-lesson02-html.png)

很明显，其新闻内容都在`<div class="pic-content">`里面，段落使用`<p>`标签，理解了这点就可以抽取详情的内容了。

这个实现起来并不难，只需要修改爬虫的parse部分即可：

```python
    def parse(self, response):
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
            yield scrapy.request(url[0],
                                 meta={'item': item},
                                 callback=self.parse_desc)

    def parse_desc(self, response):
        """抽取详情"""
        item = response.meta['item']
        desc = response.xpath("//div[@class='pic-content']/p//text()").extract()
        desc = "\n".join(desc)
        item['desc'] = desc
        yield item
```

注：这里省略了部分代码。

这里关键需要理解:

- 列表页面是怎么将数据传到详情页面的，这是meta参数的作用。
- 他们之间的调用逻辑是怎么样的

重新运行爬虫，就能看到详情页已经被我们抓取到了。


