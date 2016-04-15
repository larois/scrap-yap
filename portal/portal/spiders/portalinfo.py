# -*- coding: latin-1 -*-
import scrapy
import math
from scrapy.selector import Selector
from scrapy.http import Request
from portal.items import PortalInfo 


class PortalinfoSpider(scrapy.Spider):
    name = "portalinfo"
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
            yield Request(url, callback = self.parseListing)

    def parseListing(self, response):
        for constructora in response.css("tr[id*=ContentPlaceHolder1_ListViewCorredorasPresentes_ctr] td"):
            inmo_view =  constructora.css('a::attr(href)').extract()[0]
            inmo_name = constructora.css("a img::attr(title)").extract()[0]
            inmo_url_view = "http://www.portalinmobiliario.com" + inmo_view
            yield Request(inmo_url_view, meta={'name': inmo_name, 'url_view': inmo_url_view}, callback = self.parseView)
            
    def parseView(self, response):
        contact = response.css(".Valor::text").extract()
        item = PortalInfo()
        item["inmo_name"] = response.meta['name']
        item["inmo_url_view"] = response.meta['url_view']
        item["inmo_contact"] = contact
        return item



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
