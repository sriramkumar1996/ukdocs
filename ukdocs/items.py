import scrapy


class DocItem(scrapy.Item):
    title = scrapy.Field()
    date_published = scrapy.Field()
    url = scrapy.Field()
    pdf = scrapy.Field()
    summary = scrapy.Field()

    def set_all(self, value):
        for keys, _ in self.fields.items():
            self[keys] = value

