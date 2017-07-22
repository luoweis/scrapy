# 爬虫
## 安装
```
virtualenv --no-site-packages venv
source venv/bin/active
pip install Scrapy
```
### 创建一个scrapy项目
```
scrapy startproject scrapyTest
创建一个爬虫文件
scrapy genspider luoweis www.shiluowei.cn
爬虫name='luoweis'
start_url = 'http://www.shiluowei.cn'

scrapy crawl luoweis -o luoweis.json| luoweis.jl
开始爬取 并保存到项目中

scrapy check
检查scrapy爬虫文件是否有错误

scrapy list
列出现有的爬虫名称


```

### 项目目录
```
scrapyTest/
├── scrapy.cfg  #配置文件
└── scrapyTest  #项目主目录
    ├── __init__.py
    ├── items.py    #定义项目文件
    ├── middlewares.py #中间件
    ├── pipelines.py    #管道
    ├── settings.py     #配置文件
    └── spiders         #爬虫文件
        └── __init__.py
```
### 创建一个spider
在scrapyTest/scrapyTest/spiders/目录下创建一个spider文件
spider_quotes.py

```
#!/usr/bin/env python
# -*- coding: utf-8 -*

#spider的测试用例

import scrapy

class SpiderQuotes(scrapy.Spider):
    '''
    定义名字
    名字在整个项目目录中必须是唯一的
    这个名字定义的是这个spider的名字
    '''
    name = "quotes"
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    #专门用来下载爬取到的页面内容的函数方法
    def parse(self, response):
        page = response.url.split("/")[-2]
        #['http:', '', 'quotes.toscrape.com', 'page', '1', '']
        filename = 'quotes-%s.html' % page
        with open(filename,'wb') as f:
            f.write(response.body)
        self.log('保存文件：%s' %filename)
```

#### 运行爬虫
```
scrapy crawl quotes
"quotes" 为我们定义的爬虫名字
```
#### 运行流程
```
启动扩展插件=》启动下载中间件=》启动爬取中间件=》启动项目管道中间件=》最后将爬取的网页保存在本地目录中
```

#### css模块
```
#!/usr/bin/env python
# -*- coding: utf-8 -*

#spider的测试用例

import scrapy
from pprint import pprint

class SpiderQuotes(scrapy.Spider):
    #'''
    #定义名字
    #名字在整个项目目录中必须是唯一的
    #这个名字定义的是这个spider的名字
    #'''
    name = "quotes"
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    #专门用来下载爬取到的页面内容的函数方法
    def parse(self, response):
        # page = response.url.split("/")[-2]
        # #['http:', '', 'quotes.toscrape.com', 'page', '1', '']
        # filename = 'quotes-%s.html' % page
        # with open(filename,'wb') as f:
        #     f.write(response.body)
        # self.log('保存文件：%s' %filename)

        #尝试输出我们制定需要的html内容
        #输出网页的title

        title = response.css('title')
        pprint(title)

        #输出信息：[ < Selector xpath = u'descendant-or-self::title' data = u'<title>Quotes to Scrape</title>' >]

        title_getOnly_html=response.css('title').extract()
        pprint(title_getOnly_html)
        #输出信息：[u'<title>Quotes to Scrape</title>']

        title_without_html = response.css('title::text').extract()
        pprint(title_without_html)
        #输出信息 [u'Quotes to Scrape'] scrapy会去掉html表示显示纯文本内容

        #此时是显示的一个列表
        title_without_html_first = response.css('title::text').extract_first()
        pprint(title_without_html_first)
        #输出数据：u'Quotes to Scrape'
        #输出列表的第一个数据
        #.extract_first()的能避免IndexError异常错误，并且如果没有匹配时你能自动放回None

```

#### 本地持久化保存JSON数据
```
#!/usr/bin/env python
# -*- coding: utf-8 -*

#spider的测试用例

import scrapy
from pprint import pprint

class SpiderQuotes(scrapy.Spider):
    '''
    定义名字
    名字在整个项目目录中必须是唯一的
    这个名字定义的是这个spider的名字
    '''
    name = "quotes"
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    #专门用来下载爬取到的页面内容的函数方法
    def parse(self, response):
        res = {}
        all = []
        quotes = response.css("div.quote")
        for quote in quotes:
            #div 表示html的标签
            #quote 表示类名字
            content = quote.css("span.text::text").extract_first()
            author = quote.css("small.author::text").extract_first()
            tags = quote.css("div.tags a.tag::text").extract()
            #触发一个生成器 将每条每个quote中的相关内容封装成一个dic
            yield {
                'content':content,
                'author':author,
                'tags':tags
            }

        """
        {'author': u'Albert Einstein',
        'content': u'\u201cThe world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.\u201d',
        'tags': [u'change', u'deep-thoughts', u'thinking', u'world']}
        """
```

    scrapy crawl quotes -o quotes.json
    会全部反复追加到quotes.json文件中，运行两边命令会造成一个破坏了的json格式数据文件
    scrapy crawl quotes -o quotes.jl
    JSON Lines 模式的文件，数据流，每条数据是单独的的进行追加，不会破坏json文件的完整性。

#### 追踪链接

```
#!/usr/bin/env python
# -*- coding: utf-8 -*

#spider的测试用例

import scrapy
from pprint import pprint

class SpiderQuotes(scrapy.Spider):

    name = "quotes"
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com',
        ]

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    #专门用来下载爬取到的页面内容的函数方法
    def parse(self, response):
        quotes = response.css("div.quote")
        for quote in quotes:
            #div 表示html的标签
            #quote 表示类名字
            content = quote.css("span.text::text").extract_first()
            author = quote.css("small.author::text").extract_first()
            tags = quote.css("div.tags a.tag::text").extract()
            #触发一个生成器 将每条每个quote中的相关内容封装成一个dic
            yield {
                'content':content,
                'author':author,
                'tags':tags
            }
        #默认爬取的是首页的内容
        #通过以下操作取根据链接爬取下一页的内容
        #定义下一页
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)#链接拼接，自动拼接成一个完整的url
            yield scrapy.Request(url=next_page,callback=self.parse)

        #通过不断回调函数的方式，不断的取爬取下一页的链接内容。

```
    这里通过response.urljoin的方式将获取的相对路径链接拼接成了绝对路径，只有这样才能通过scrapy.Request()的方法取爬取内容。
    可以通过response.follow()的方法使用短链接取爬取对应的页面


