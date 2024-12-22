import scrapy

class PUSpider(scrapy.Spider):
    name = "pu_spider"
    start_urls = ["https://pu.edu.pk/page"]

    def parse(self, response):
        # Extract the introduction text
        descriptions = response.css('td > div[align="justify"]::text').getall()
        full_description = " ".join(descriptions).strip()

        homepage_url = "https://pu.edu.pk/"
        yield scrapy.Request(
            url=homepage_url,
            callback=self.parse_homepage,
            meta={"introduction": full_description}
        )

    def parse_homepage(self, response):
        university_title = response.css('title::text').get().strip()
        main_link = response.xpath('//*[@id="logo"]/h1/a/@href').get()

        # Extract social media links
        instagram_link = response.xpath('//*[@id="header"]/div[2]/div[1]/ul/li[4]/a/@href').get()
        facebook_link = response.xpath('//*[@id="header"]/div[2]/div[1]/ul/li[2]/a/@href').get()
        twitter_link = response.xpath('//*[@id="header"]/div[2]/div[1]/ul/li[3]/a/@href').get()

        # Hard-code the ranking value
        ranking = "3"

        # Define contact page URL
        contact_page_url = "https://pu.edu.pk/page/show/contact-us.html"

        # Define campuses page URL
        campuses_page_url = "https://pu.edu.pk/page/show/Campuses.html"

        yield scrapy.Request(
            url=contact_page_url,
            callback=self.parse_contact,
            meta={
                "university_title": university_title,
                "main_link": main_link,
                "social_links": {
                    "instagram": instagram_link,
                    "facebook": facebook_link,
                    "twitter": twitter_link
                },
                "ranking": ranking,
                "introduction": response.meta["introduction"],
                "campuses_page_url": campuses_page_url
            }
        )

    def parse_contact(self, response):
        # Extract contact details
        info_email = response.xpath('//*[@id="ntb"]/tbody/tr[7]/td[1]/span/span/font/a/font/text()').get()
        call_number = response.xpath('//*[@id="ntb"]/tbody/tr[6]/td[2]/span/span/font/font/text()').get()

        # Pass the campuses data and other details to the next step
        campuses_page_url = response.meta["campuses_page_url"]
        yield scrapy.Request(
            url=campuses_page_url,
            callback=self.parse_campuses,
            meta={
                "university_title": response.meta["university_title"],
                "main_link": response.meta["main_link"],
                "social_links": response.meta["social_links"],
                "ranking": response.meta["ranking"],
                "introduction": response.meta["introduction"],
                "info_email": info_email,
                "call_number": call_number
            }
        )

    def parse_campuses(self, response):
        # Extract campus links
        new_campus = response.xpath('//table//tr[2]/td[1]/a/@href').get()
        old_campus = response.xpath('//table//tr[2]/td[3]/a/@href').get()
        gujranwala_campus = response.xpath('//table//tr[3]/td[1]/a/@href').get()
        khanspur_campus = response.xpath('//table//tr[3]/td[3]/a/@href').get()
        jhelum_campus = response.xpath('//table//tr[4]/td[1]/div/a/@href').get()
        pothohar_campus = response.xpath('//table/tbody/tr[4]/td[3]/div/a/@href').get()

        # Yield the full data in JSON format
        yield {
            "university_title": response.meta["university_title"],
            "main_link": response.meta["main_link"],
            "social_links": response.meta["social_links"],
            "ranking": response.meta["ranking"],
            "contact_details": {
                "info_email": response.meta["info_email"],
                "call": response.meta["call_number"]
            },
            "introduction": response.meta["introduction"],
            "campuses": {
                "new_campus": new_campus,
                "old_campus": old_campus,
                "gujranwala_campus": gujranwala_campus,
                "khanspur_campus": khanspur_campus,
                "jhelum_campus": jhelum_campus,
                "pothohar_campus": pothohar_campus
            }
        }
