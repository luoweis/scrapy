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


        #将数据保存到本地
        #保存为json数据
        ###scrapy crawl quotes -o quotes.json
        #这样的方式会全部反复追加到quotes.json文件中，不会做差异化的增量工作

        ###scrapy crawl quotes -o quotes.jl
        #JSON Lines 模式的文件，数据流，每条数据是单独的的进行追加，不会破坏json文件的完整性。




