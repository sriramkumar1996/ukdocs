import json
import re
import scrapy
from ..items import DocItem
from scrapy.exceptions import UsageError
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from urllib.parse import urlencode


class NhsSpider(scrapy.Spider):
    name = 'nhs'
    allowed_domains = ['england.nhs.uk']
    error_page = open('error_page.log','a')

    def __init__(self, *args, **kwargs):
        super(NhsSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        url = 'https://www.england.nhs.uk/estates/health-building-notes/'
        yield scrapy.Request(url=url, callback=self.parse_search, method='GET', errback=self.errback_httpbin)

        url = 'https://www.england.nhs.uk/estates/health-technical-memoranda/'
        yield scrapy.Request(url=url, callback=self.parse_search, method='GET', errback=self.errback_httpbin)

        url = 'https://www.england.nhs.uk/estates/other-guidance/'
        yield scrapy.Request(url=url, callback=self.parse_search, method='GET', errback=self.errback_httpbin)

    def parse_search(self, response):
        print(response.url)
        results = response.css('div#main-content article > ul > li a::attr(href)').extract()
        for url in results:
            if url.startswith('https:'):
                meta = {
                    'url': url,
                }
                yield scrapy.Request(url=url, callback=self.parse_data, meta=meta, method='GET', errback=self.errback_httpbin)

    def parse_data(self, response):
        print(response.url)
        meta = dict(response.meta)

        item = DocItem()
        item.set_all(None)

        title = response.css('section#main-content header h1::text').extract_first()
        item['title'] = self.filter_text(title) 
        item['url'] = meta['url']

        dl = response.css('div.publishing-meta dl.group')
        if len(dl) > 0:
            dt_list = dl[0].css('dt')
            dd_list = dl[0].css('dd')

            if len(dt_list) == len(dd_list):
                for i in range(0, len(dt_list)):
                    key = dt_list[i].css('dt::text').extract_first()
                    if 'published' in key:  
                        item['date_published'] = dd_list[i].css('dd time::attr(datetime)').extract_first()


        docs = response.css('section#main-content div.document-content div.document-thumbnail.group')
        if len(docs) > 0:
            for doc in docs:    
                pdf = doc.css('div.document-file.group div.summary a.doc-thumbnail::attr(href)').extract_first()
                if pdf:
                    summary = doc.css('div.document-summary.group div.content.rich-text * ::text').extract()
                    item['summary'] = self.filter_text(summary)
                    item['pdf'] = pdf
                    yield item

    def filter_text(self, text):
        if isinstance(text, list):
            if len(text) > 0:   
                return self.filter_text((' ').join(text))
            return None
        else:
            if text != None:
                text = text.replace(u'\n', u' ')
                text = text.replace(u'\t', u' ')
                text = text.replace(u'<br>', u' ')
                text = ' '.join(text.split())
        return text

    def filter_summary(self, text):
        if isinstance(text, list):
            if len(text) > 0:
                text = list(filter(lambda x: x != '\n', text))
                return '\n\n'.join(text)
        return None

    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
            self.error_page.write(response.url+'\n')
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
            self.error_page.write(request.url+'\n')
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.error_page.write(request.url+'\n')
    

