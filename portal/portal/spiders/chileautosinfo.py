# -*- coding: latin-1 -*-
import scrapy
import math
from scrapy.selector import Selector
from scrapy.http import Request
from portal.items import ChileAutosInfo 


class ChileautosinfoSpider(scrapy.Spider):
    name = "chileautosinfo"
    allowed_domains = ["chileautos.cl"]
    start_urls = (
        'http://www2.chileautos.cl/cslocal.asp',
    )
    
    def parse(self, response):
        for automotora in response.css(".divtotal .divtexto"):
            auto_url = "http://www2.chileautos.cl/" + automotora.css('a::attr(href)').extract()[0]
            meta={'url': auto_url}
            yield Request(auto_url, meta=meta, callback = self.parseView)
            
    def parseView(self, response):
        elem_ads = response.css("div.contenedor_tablaautosautomotora > div > span:nth-child(1) > font:nth-child(1)::text").extract()
        total_ads = 0
        if isinstance(elem_ads, list) and len(elem_ads) > 0:
            total_ads = int(elem_ads[0])
        total_pages = total_ads/40
        if total_pages > 0:
            print "corredora top {} ".format(total_ads)

        name = response.css("h1::text").extract()
        item = ChileAutosInfo()
        item["name"] = name
        item["url"] = response.meta['url'] 
        item["total_ads"] = total_ads
        return item
