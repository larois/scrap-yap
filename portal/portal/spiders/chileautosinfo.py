# -*- coding: latin-1 -*-
import scrapy
import math
from scrapy.selector import Selector
from scrapy.http import Request
from portal.items import ChileAutosInfo 
import re


class ChileautosinfoSpider(scrapy.Spider):
    name = "chileautosinfo"
    allowed_domains = ["chileautos.cl"]
    start_urls = (
        'https://www.chileautos.cl/automotoras/buscar',
    )
    
    def parse(self, response):
        for automotora in response.css(".dealer-search-item.listing-item"):
            auto_url = automotora.css('.listing-item__header a::attr(href)').extract()[0]
            auto_name = automotora.css('.listing-item__header a h2::text').extract()
            meta = {
                'url': auto_url,
                'name': auto_name
            }
            yield Request(auto_url, meta=meta, callback=self.parseView)
            
    def parseView(self, response):
        elem_ads = response.css(".page-header span::text").extract()[0]
        if 'venta' not in elem_ads:
            elem_ads = '0'

        item = ChileAutosInfo()
        item["name"] = response.meta['name']
        item["url"] = response.meta['url'] 
        item["total_ads"] = int(re.search(r'\d+', elem_ads).group())
        return item
