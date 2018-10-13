# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
from ..items import DailiItem
import requests


class XiciSpider(CrawlSpider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn/']
    rules = (
        Rule(LinkExtractor(allow=r'^http://www.xicidaili.com/nn/[2-3]?$'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # # xpath
        # ip_list = response.xpath('//table[@id="ip_list"]//tr[@class="odd" or @class=""]/td[2]/text()').extract()
        # port_list = response.xpath('//table[@id="ip_list"]//tr[@class="odd" or @class=""]/td[3]/text()').extract()
        # type_list = response.xpath('//table[@id="ip_list"]//tr[@class="odd" or @class=""]/td[6]/text()').extract()

        # css
        html = response.css('#ip_list tr:not(:first-child)')
        ip_list = html.css('td:nth-child(2)::text').extract()
        port_list = html.css('td:nth-child(3)::text').extract()
        type_list = html.css('td:nth-child(6)::text').extract()

        for (ip_, port_, type_) in zip(ip_list, port_list, type_list):
            proxies = {type_ : ip_ + port_}
            try:
                if requests.get('http://www.baidu.com', proxies=proxies, timeout= 3).status_code == 200:
                    print("***Success:" + type_ + "://" + ip_ + ":" +port_ )
                    item = DailiItem()
                    item["ip_"] = ip_
                    item["port_"] = port_
                    item["type_"] = type_
                    yield item
            except:
                print("***Failure:" + type_ + "://" + ip_ + ":" + port_ )


