# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class SuperMamiItem(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(str.strip, lambda x: x.replace('$', '').strip()),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(str.strip, lambda x: x.strip()),
        output_processor=TakeFirst()
    )
    brand = scrapy.Field(
        input_processor=MapCompose(str.strip, lambda x: x.strip()),
        output_processor=TakeFirst()
    )
    branch = scrapy.Field(
        input_processor=MapCompose(str.strip, lambda x: x.strip()),
        output_processor=TakeFirst()
    )
