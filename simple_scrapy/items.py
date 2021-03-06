# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PersonItem(scrapy.Item):
    firstName = scrapy.Field()
    lastName = scrapy.Field()
    position = scrapy.Field()
    company = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
