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



