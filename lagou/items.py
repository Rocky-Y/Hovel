import scrapy


class LagouprojectItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()

