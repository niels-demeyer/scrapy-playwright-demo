import scrapy


class TweedehandsItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()


