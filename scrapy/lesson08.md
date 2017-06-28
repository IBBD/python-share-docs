# Lesson08: scrapy爬虫程序的调试
爬虫在执行的过程中可能会出现各种问题，怎么调试往往是非常重要的。下面会介绍几种调试的方式：

1. shell
2. 在浏览器中打开，查看response
3. Parse命令
4. 日志

## Scrapy Shell
爬虫最常见的问题是，抓取不到数据，这时很可能就是selector（例如xpath）写得不对。而scrapy shell就是调试这种问题的利器。

进入shell的两种方式：

- 第一种方式：直接进入shell：

```sh
scrapy shell 'https://docs.scrapy.org/en/latest/topics/debug.html'

# 指定USER_AGENT
scrapy shell -s USER_AGENT='custom user agent' 'http://www.example.com'
```

这时就会进入一下控制台，可以理解为到了爬虫的parse部分，正常情况下网页数据已经下载回来了，response对象已经生成，在控制台中都可以直接使用。

比较重要的对象包括：

1. response：结果对象，做解释时经常需要使用
2. request：请求对象，例如`request.headers`可以查看请求头的信息，例如设置的代理是否生效，user-agent是否正确等。

如果遇到xpath匹配不到内容，或者匹配到的内容不正确，我们可能还需要查看response的源码是否和我们网页上看到的一致（注意：爬虫模拟请求到的页面可能和我们在浏览器上看到的并不一致，因为可能存在终端类型适配的问题，如手机或者pc，人群适配的问题，反爬虫机制的问题等），这时可以在shell中直接存储html文件，代码很简单，如下：

```python
with open('/tmp/filename.html', 'w') as w:
    w.write(str(response.body))
```

文件路径可以选择一个方便的即可。

- 第二种方式：在爬虫中进入shell：

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

当程序执行到对应的地方的时候，就会自动进入shell环境。使用这种方式时，当从shell中退出的时候，会自动返回爬虫继续执行。这个方式就类似断点的作用，可以设置多个断点。

在shell环境内，可以很简单的进行各种xpath的实验，还可以通过`view(response)`在浏览器打开下载的页面（可以辅助xpath的提取）。

## 在浏览器中打开
前面已经说了在shell中，怎么在浏览器中打开页面，即使用`view(response)`。其实在命令行下也可以直接用浏览器打开：

```python
from scrapy.utils.response import open_in_browser

def parse_details(self, response):
    if "item name" not in response.body:
        open_in_browser(response)
```

代码实现上和进入shell中类似，这里不再详述。

可以根据这里的显示，提取xpath，查看download的页面是否正常等。

## Parse命令
到目前为止，我们常用的命令是`crawl`和`shell`，这两个命令，一个是启动爬虫，一个是启动shell。

不过有时在测试或者调试的时候，并不一定期望进入shell去调试。例如，爬虫分页抓取新闻的列表页面，然后又根据url抓取新闻的详情页面，但是在抓取某个详情页面的时候，却出现了抓取不到数据的异常（或者抓取不全的异常）。

```sh
scrapy parse --spider=movieNews -c parse_desc -a catid=220 -d 2 -v 'http://www.1905.com/news/20170502/1178888.shtml'
```

执行`scrapy parse`即可查看到上面参数的解释。爬虫会直接下载对应url，并调用相应的解释函数进行处理（-c指定的参数，这里是parse_desc），方便调试。

注：不过这里也有一个局限，就是无法指定meta值，所以在parse函数中也需要接受来自父页面的meta值，就不太适合使用该方法了。

## 日志
日志也是调试程序的利器，具体在日志部分有详述，这里不罗嗦。

