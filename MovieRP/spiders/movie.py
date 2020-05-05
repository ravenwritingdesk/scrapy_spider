# coding: utf-8
# Copyright © 2020- by Wangchuwen. All rights reserved
import scrapy
from MovieRP.items import MovierpItem


class movierpSpider(scrapy.Spider):
    # 爬虫名称
    name = 'movie'
    # 爬虫允许爬取域名
    allowed_domains = ['movie.douban.com']
    # 基础域名
    base_url = 'https://movie.douban.com/subject/11537954/comments'
    # 爬虫起始URL
    start_urls = ['https://movie.douban.com/subject/11537954/comments?status=P']
    # 爬虫页数控制初始值
    count = 1
    # 爬虫爬取页数
    spider_end = 3

    def parse(self, response):

        item = MovierpItem()

        # 下一页地址
        nextPage = self.base_url + response.xpath("//div[@id='paginator']/a[@class='next']/@href").extract()[0]

        # 提取短评信息
        node_list = response.xpath('//div[@class="comment"]')
        for node in node_list:
            item['name'] = node.xpath('./h3/span[@class="comment-info"]/a/text()').extract()[0]
            item['content'] = node.xpath('./p/span[@class="short"]/text()').extract()[0]
            yield item


        # 爬虫页数控制及末页控制
        if self.count < self.spider_end:
            # 爬虫页数控制自增    
            self.count = self.count + 1

            # 爬取下一页
            yield scrapy.Request(nextPage, callback=self.parse)
        else:
            # 爬虫退出
            return None