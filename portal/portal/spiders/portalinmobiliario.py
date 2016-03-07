# -*- coding: utf-8 -*-
import scrapy
import math
from scrapy.selector import Selector
from scrapy.http import Request
from portal.items import PortalItem 


class PortalinmobiliarioSpider(scrapy.Spider):
    name = "portalinmobiliario"
    allowed_domains = ["portalinmobiliario.com"]
    start_urls = (
        'http://www.portalinmobiliario.com/empresas/corredoraspresentes.aspx',
    )
    
    def parse(self, response):
        num_items = response.css("#ContentPlaceHolder1_lblNumeroCorredorasPresentes font::text").extract()
        total_pages = float(num_items[0]) / 15.0
        total_pages = int(math.ceil(total_pages)) + 1
        print("total pages: {0}".format(total_pages))
        urls = ['http://www.portalinmobiliario.com/empresas/corredoraspresentes.aspx?p=%d' %(n) for n in range(1, total_pages)]
        for url in urls:
            yield Request(url, callback = self.parsePage)

    def parsePage(self, response):
        items = []
        for constructora in response.css("tr[id*=ContentPlaceHolder1_ListViewCorredorasPresentes_ctr] td"):
            item = PortalItem()
            item["url"] = "http://www.portalinmobiliario.com" + constructora.css('a::attr(href)').extract()[0]
            item["name"] = constructora.css("a img::attr(title)").extract()[0]
            items.append(item)
        return items
            



"""
        hxs = HtmlXPathSelector(response)

        next_page = hxs.select("//div[@class='pagination']/a[@class='next_page']/@href").extract()
        if next_page:
            yield Request(next_page[0], self.parse)

        posts = hxs.select("//div[@class='post']")
        items = []
        for post in posts:
            item = ScrapySampleItem()
            item["title"] = post.select("div[@class='bodytext']/h2/a/text()").extract()
            item["link"] = post.select("div[@class='bodytext']/h2/a/@href").extract()
            item["content"] = post.select("div[@class='bodytext']/p/text()").extract()
            items.append(item)
        for item in items:
            yield item
        pass
"""
