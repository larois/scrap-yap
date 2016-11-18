# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PortalItem(scrapy.Item):
    inmo_name = scrapy.Field()
    inmo_url_view = scrapy.Field()
    inmo_url = scrapy.Field()
    commune_name = scrapy.Field()
    commune_url = scrapy.Field()
    commune_total_ads = scrapy.Field()
    pass

class PortalInfo(scrapy.Item):
    inmo_name = scrapy.Field()
    inmo_url_view = scrapy.Field()
    inmo_contact = scrapy.Field()
    pass

class ChileAutosInfo(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    total_ads = scrapy.Field()
    pass
