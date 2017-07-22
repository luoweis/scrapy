#!/usr/bin/env python
# -*- coding: utf-8 -*

#spider的测试用例
#使用xpath方法
import scrapy

class SpiderQuotesXpath(scrapy.Spider):
    name = "quotesXpath"
    def start_requests(self):
        start_urls = [
            "http://quotes.toscrape.com/",
        ]
        for url in start_urls:
            yield scrapy.Request(url=url,callback=self.parse)


    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text':quote.xpath('./span[@class="text"]/text()').extract_first(),
                'author':quote.xpath('.//small[@class="author"]/text()').extract_first(),
                'tags':quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            }

        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            yield response.follow(url=next_page,callback=self.parse)



#scrapy crawl quotesXpath
