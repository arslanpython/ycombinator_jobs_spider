from scrapy import Field, Item


class JobItem(Item):
    job_id = Field()
    name = Field()
    location = Field()
    position = Field()
