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
            'http://quotes.toscrape.com',
            # 'http://quotes.toscrape.com/page/2/',
        ]

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    #专门用来下载爬取到的页面内容的函数方法
    def parse(self, response):
        quotes = response.css("div.quote")
        # 定义下一页
        next_page = response.css('li.next > a::attr(href)').extract_first()
        for quote in quotes:
            #div 表示html的标签
            #quote 表示类名字
            content = quote.css("span.text::text").extract_first()
            author = quote.css("small.author::text").extract_first()
            tags = quote.css("div.tags > a.tag::text").extract()

            #触发一个生成器 将每条每个quote中的相关内容封装成一个dic
            yield {
                'content':content,
                'author':author,
                'tags':tags,
                'nextPage':next_page
            }
        #默认爬取的是首页的内容
        #通过以下操作取根据链接爬取下一页的内容
        if next_page is not None:
            #这里使用response.follow() 短链接的方式
            yield response.follow(url=next_page,callback=self.parse)
        #通过不断回调函数的方式，不断的取爬取下一页的链接内容。





