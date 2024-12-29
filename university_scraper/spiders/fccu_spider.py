import scrapy

class FccuSpiderSpider(scrapy.Spider):
    name = "fccu_spider"
    allowed_domains = ["fccollege.edu.pk"]
    start_urls = ["https://www.fccollege.edu.pk/about/"]

    def parse(self, response):
        # Set the university title manually
        university_title = "FCCU"

        # Extract the main link of the university (only the first link in the list)
        main_link = response.xpath('//*[@id="wrapper"]/div[2]/div[1]/div/div[1]/div/div/span/a/@href').get()

        # Define social links with the correct XPath for each platform
        social_links = {
            "instagram_link": response.xpath('//a[contains(@href, "instagram.com")]/@href').get(),
            "facebook_link": response.xpath('//a[contains(@href, "facebook.com")]/@href').get(),
            "twitter_link": response.xpath('//a[contains(@href, "twitter.com")]/@href').get(),
            "youtube_link": response.xpath('//a[contains(@href, "youtube.com")]/@href').get(),
            "linkedin_link": response.xpath('//a[contains(@href, "linkedin.com")]/@href').get(),
        }

        # Define a ranking, or use data from a relevant source
        ranking = "not known"
        
        # Extract contact details
        info_email = response.xpath('//*[@id="custom_html-5"]/div[1]/ul/li[3]/div/a/text()').get()
        call_number = response.xpath('//*[@id="custom_html-5"]/div[1]/ul/li[2]/div/span/text()').get()

        introduction = response.xpath('//*[@id="post-2626"]/div/div[3]/div/div/div/div[1]/p/span/text()').get()

        # Yield the collected data
        yield {
            'university_title': university_title,
            'main_link': main_link,
            'social_links': social_links,
            'ranking': ranking,
            "contact_details": {
                'info_email': info_email,
                'call': call_number
            },
            'introduction': introduction
        }
