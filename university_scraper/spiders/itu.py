import scrapy

class MyWebpageSpider(scrapy.Spider):
    name = "itu_bsse"
    start_urls = ["https://itu.edu.pk/"]  # Replace with your target website URL

    def parse(self, response):
        # Extract links using XPath
        links = response.xpath('/html/body/div[6]/div[2]/div/div/div/div[1]/div/div[2]/ul/li[7]/a/@href').getall()

        # Yield each extracted link
        for link in links:
            yield {
                "link": response.urljoin(link) if link else "No link",
            }
