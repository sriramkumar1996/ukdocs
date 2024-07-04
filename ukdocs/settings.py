BOT_NAME = 'ukdocs'
SPIDER_MODULES = ['ukdocs.spiders']
NEWSPIDER_MODULE = 'ukdocs.spiders'

# LOG_LEVEL = 'WARNING'
LOG_FILE = 'error.log'

ROBOTSTXT_OBEY = False

HTTP_PROXY = 'http://127.0.0.1:8118'
# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'
# DEFAULT_REQUEST_HEADERS = {}


CONCURRENT_REQUESTS = 8
# DOWNLOAD_DELAY = 2
# CONCURRENT_REQUESTS_PER_DOMAIN = 8
# CONCURRENT_REQUESTS_PER_IP = 8


DOWNLOADER_MIDDLEWARES = {
	'ukdocs.middlewares.ProxyMiddleware': 543,
	'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
	'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

ITEM_PIPELINES = {
	'ukdocs.pipelines.UkdocsPipeline': 300,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

