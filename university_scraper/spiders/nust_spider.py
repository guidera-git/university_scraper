import scrapy

class NustSpider(scrapy.Spider):
    name = 'nust_spider'
    start_urls = ['https://nust.edu.pk/']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'ROBOTSTXT_OBEY': False,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'nust.edu.pk',
            'Upgrade-Insecure-Requests': '1'
        },
    }

    def parse(self, response):
        self.log('Visited %s' % response.url)
        # Your parsing logic here
