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

#### 扩展内容
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