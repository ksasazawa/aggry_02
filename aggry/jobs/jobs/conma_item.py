import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join

class Jobs(scrapy.Item):
    title = scrapy.Field(
        output_processor = TakeFirst()
    )
    job = scrapy.Field(
        output_processor = TakeFirst()
    )
    location = scrapy.Field(
        output_processor = TakeFirst()
    )
    price = scrapy.Field(
        output_processor = TakeFirst()
    )
    detail = scrapy.Field(
        output_processor = TakeFirst()
    )
    welfare = scrapy.Field(
        output_processor = TakeFirst()
    )
    agent = scrapy.Field(
        output_processor = TakeFirst()
    )
    agent_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    url = scrapy.Field(
        output_processor = TakeFirst()
    )
    data_added = scrapy.Field(
        output_processor = TakeFirst()
    )

