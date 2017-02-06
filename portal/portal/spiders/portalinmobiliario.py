# -*- coding: latin-1 -*-
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
            yield Request(url, callback = self.parseListing)

    def parseListing(self, response):
        for constructora in response.css("tr[id*=ContentPlaceHolder1_ListViewCorredorasPresentes_ctr] td"):
            inmo_view =  constructora.css('a::attr(href)').extract()[0]
            inmo_name = constructora.css("a img::attr(title)").extract()[0]
            inmo_url_view = "http://www.portalinmobiliario.com" + inmo_view
            inmo_url = "http://www.portalinmobiliario.com/propiedades/broker_fic.asp?" + inmo_view.split("?")[1]
            yield Request(inmo_url, meta={'name': inmo_name, 'url_view': inmo_url_view, 'url': inmo_url}, callback = self.parseView)
            
    def parseView(self, response):
        inmo_name = response.meta['name']
        inmo_url_view = response.meta['url_view']
        inmo_url = response.meta['url']
        for commune in response.css("table td [href*='Buscar_resp']"):
            commune_name = commune.css('a::text').extract()[0]
            commune_url =  commune.css('a::attr(href)').extract()[0]
            commune_url = "http://www.portalinmobiliario.com" + commune_url.replace("..", "")
            data = {
                    'name': inmo_name, 
                    'inmo_url_view': inmo_url_view,
                    'inmo_url': inmo_url,
                    'commune': commune_name, 
                    'commune_url': commune_url
            }
            yield Request(commune_url, meta=data, callback = self.parseCommune)

    def parseCommune(self, response):
        num_items = response.css("#tableListadoPropiedades .RGBPaginacionFilaGris > td:nth-child(1) > b::text").extract()[0]
        num_items = num_items.replace("\r\n", "")
        num_items = num_items.replace(",", "")
        totals = [int(s) for s in num_items.split() if s.isdigit()]
        item = PortalItem()
        item["inmo_name"] = response.meta['name']
        item["inmo_url_view"] = response.meta['inmo_url_view']
        item["inmo_url"] = response.meta['inmo_url']
        item["commune_name"] = response.meta['commune']
        item["commune_url"] = response.meta['commune_url']
        item["commune_total_ads"] = totals[0]
        return item
