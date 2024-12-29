import scrapy

class ComsatsSpiderSpider(scrapy.Spider):
    name = "comsats_spider"
    allowed_domains = ["comsats.edu.pk"]
    start_urls = ["https://comsats.edu.pk"]

    def parse(self, response):
        # Extract the university title
        university_title = response.xpath('//*[@id="header"]/div/a/h5/text()').get().strip()

        # Main link of the university
        main_link = "https://www.comsats.edu.pk/"
        
        # Define social links with the correct XPath for each platform
        social_links = {
            "instagram_link": response.xpath('//*[@id="footer"]/div[1]/div/div/div[5]/div/a[3]/@href').get(),
            "facebook_link": response.xpath('//a[contains(@href, "facebook.com")]/@href').get(),
            "twitter_link": response.xpath('//a[contains(@href, "twitter.com")]/@href').get(),
            "youtube_link": response.xpath('//a[contains(@href, "youtube.com")]/@href').get(),
        }
        
        ranking = "not known"
        
        # Yield the data and proceed to the "Contact Us" page
        yield scrapy.Request(
            url="https://www.comsats.edu.pk/contactus.aspx",
            callback=self.parse_contact_us,
            meta={
                'university_title': university_title,
                'main_link': main_link,
                'social_links': social_links,
                'ranking': ranking
            }
        )

    def parse_contact_us(self, response):
        # Extract contact details from the "Contact Us" page
        info_email = response.xpath('//strong[text()="Email:"]/following-sibling::text()').get()
        call_number = response.xpath('//strong[text()="Phone:"]/following-sibling::text()').get()

        # Proceed to the "About Us" page
        yield scrapy.Request(
            url="https://www.comsats.edu.pk/about-comsats.aspx",
            callback=self.parse_about_us,
            meta={
                'university_title': response.meta['university_title'],
                'main_link': response.meta['main_link'],
                'social_links': response.meta['social_links'],
                'ranking': response.meta['ranking'],
                "contact_details": {
                    "info_email": info_email,
                    "call": call_number
                }
            }
        )

    def parse_about_us(self, response):
        # Extract the introduction paragraph(s)
        intro_paragraphs = response.xpath('//*[@id="main"]/section[3]/div/div/div[1]/div/div[2]//text()').getall()
        introduction = " ".join([p.strip() for p in intro_paragraphs if p.strip()])  # Join non-empty parts

        # Combine data from the previous request
        yield {
            'university_title': response.meta['university_title'],
            'main_link': response.meta['main_link'],
            'social_links': response.meta['social_links'],
            'ranking': response.meta['ranking'],
            "contact_details": response.meta['contact_details'],
            'introduction': introduction
        }
