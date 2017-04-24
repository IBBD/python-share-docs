# Lesson01: 实现一个简单的爬虫程序

## 课程目标：抓取影视新闻列表

- 抓取的URL：http://www.1905.com/list-p-catid-220.html
- 抓取的内容：新闻标题，日期，详情等

## 安装scrapy
安装过程很简单，python环境安装好之后，只需要一个命令即可：

```sh
pip install scrapy
```

## 实现过程

- 1. 创建项目

使用scrapy提供的工具创建项目, `startproject`就是创建项目的命令：

```sh
scrapy startproject lesson01
```

该命令正常执行的话，会输出如下结果：

```
New Scrapy project 'lesson01', using template directory '/usr/local/lib/python3.5/dist-packages/scrapy/templates/project', created in:
    /var/www/github/ibbd/python-share-docs/scrapy/lesson01

You can start your first spider with:
    cd lesson01
    scrapy genspider example example.com
```

表示一个新的项目已经创建好了，`ls`命令查看就能发现多了一个`lesson01`的子目录。

其目录结构如下：

```
lesson01/
    scrapy.cfg            # deploy configuration file

    lesson01/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
```

- 2. 创建爬虫

scrapy同样提供了创建爬虫的工具，能节省写代码的时间：

```sh
# 进入项目目录
cd lesson01

# 创建电影新闻的爬虫，名为movieNews，对应的域名是www.1905.com
crapy genspider movieNews www.1905.com
```

这时在`lesson01/spiders/`目录下会增加一个文件`movieNews.py`的文件，就是爬虫的基础框架。代码如下：

```python
import scrapy

class MovienewsSpider(scrapy.Spider):
    name = "movieNews"
    allowed_domains = ["www.1905.com"]
    start_urls = ['http://www.1905.com/']

    def parse(self, response):
        pass
```

- 3. 实现内容抽取

要实现页面内容抽取，首先我们得了解页面的结构，我们看到的是这样的：

![页面截图](/scrapy/_images/lesson01-page.png)

查看源码，其html代码结构如（注意：下面代码省略了一下我们所不需要的代码）：

```html
<ul class="pic-event-over">

<li class="pic-pack-out ">
    <div class="pic-pack-inner">
        <h3>
            <a data-hrefexp="fr=wwwnews_newslist_news_2_201504" href="http://www.1905.com/news/20170424/1177057.shtml" title="中国年轻人遇见好莱坞前沿工艺 成龙A计划收官" target="_blank" class="title">中国年轻人遇见好莱坞前沿工艺 成龙A计划收官</a>
        </h3>
        <p>4月18日至4月22日，“成龙A计划”新晋电影人实战特训营第二期，伴随着最后一天“电影制作流程标准化：好莱坞VS中国”的高端论坛圆满结束。此次的特训营...</p>
        <div class="rel-other clear">
            <span class="timer fl">2017-04-24</span>
            <a data-hrefexp="fr=wwwnews_index_newsarea_3_201410" class="type-url fl"  target="_blank" href="http://www.1905.com/tag/tag-p-tagid-1212946.html">成龙A计划</a>
        </div>
    </div>
</li>

// 更多的li

</ul>
```

很显然，这是使用ul/li进行组织的页面，这样基于第2步已有的基础代码，我们实现如下：

```python
import scrapy

class MovienewsSpider(scrapy.Spider):
    name = "movieNews"
    allowed_domains = ["www.1905.com"]
    start_urls = ['http://www.1905.com/list-p-catid-220.html']

    def parse(self, response):
        # 特别注意li的class名字后面有一个空格，这是一个坑
        li_list = response.xpath("//ul[@class='pic-event-over']/li[@class='pic-pack-out ']/div[@class='pic-pack-inner']")

        data = []
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

        print(data)
```

至此，我们的爬虫算是有模有样了，运行起来看看效果：

```sh
scrapy crawl movieNews
```

该命令输出的信息比较多，涉及程序print出来的数据如下：

```
[
    {'title': '再现真实历史 史诗电影《血战湘江》河北巡回展...', 'url': 'http://www.1905.com/news/20170424/1177156.shtml', 'date': '2017-04-24'}, 
    {'title': '万达原力北影节联手 打造国产3D动画《妈妈咪鸭...', 'url': 'http://www.1905.com/news/20170424/1177145.shtml', 'date': '2017-04-24'}, 
    {'title': '品质良莠不齐超半数难回本 网络电影路在何方？', 'url': 'http://www.1905.com/news/20170424/1177124.shtml', 'date': '2017-04-24'}, 
    {'title': '《记忆大师》黄渤穿越未来玩直播 许玮甯拍戏溺...', 'url': 'http://www.1905.com/news/20170424/1177129.shtml', 'date': '2017-04-24'}, 
    {'title': '"麻烦小铺"开张 黄磊携《麻烦家族》现身"叫卖"', 'url': 'http://www.1905.com/news/20170424/1177122.shtml', 'date': '2017-04-24'}, 
    {'title': '中国年轻人遇见好莱坞前沿工艺 成龙A计划收官', 'url': 'http://www.1905.com/news/20170424/1177057.shtml', 'date': '2017-04-24'}
]
```



