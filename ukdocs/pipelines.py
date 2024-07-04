import csv
import json
from .items import DocItem
from datetime import date


class UkdocsPipeline:
    def __init__(self):
        pass

    def open_spider(self, spider):
        filename = 'data/' + date.today().strftime("%Y%m%d") + '-' + spider.name + '.csv'
        self.filename = open(filename, mode='w', encoding='utf_8')
        self.csv_writer = csv.writer(self.filename, quoting=csv.QUOTE_ALL)
        self.csv_writer.writerow(['Title', 'Publication Date', 'Document Link', 'PDF Link', 'Summary'])


    def close_spider(self, spider):
        self.filename.close()

    def process_item(self, item, spider):
        if isinstance(item, DocItem):
            self.csv_writer.writerow([item['title'], item['date_published'], item['url'], item['pdf'], item['summary']])

