# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SuperMamiItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    branch = scrapy.Field()