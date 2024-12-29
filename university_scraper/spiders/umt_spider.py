import scrapy
from w3lib.html import remove_tags

class UmtSpiderSpider(scrapy.Spider):
    name = "umt_spider"
    start_urls = ["https://umt.edu.pk/introducing-umt.aspx"]

    def parse(self, response):
        # Extract and clean the description from the page
        raw_description = response.css('#ctl00_cphContent_pnlArticle').get()
        full_description = remove_tags(raw_description).strip() if raw_description else "Description not found"
        formatted_description = " ".join(full_description.split())

        # Define homepage URL
        homepage_url = "https://umt.edu.pk/"

        # Pass the cleaned and formatted introduction to the next request
        yield scrapy.Request(
            url=homepage_url,
            callback=self.parse_homepage,
            meta={"introduction": formatted_description}
        )

    def parse_homepage(self, response):
        # Retrieve the introduction text from the meta
        introduction = response.meta.get("introduction")
        main_link = "https://umt.edu.pk/"

        # Extract and clean university title
        raw_title = response.css('title::text').get()
        university_title = " ".join(raw_title.split()) if raw_title else "Unknown Title"

        # Log the introduction and university title
        self.log(f"University Title: {university_title}")
        self.log(f"Introduction text: {introduction}")

        # Extract social media links
        social_links = {
            "instagram": response.xpath('//*[@id="footer-Social"]/div/ul/li[4]/a/@href').get(),
            "facebook": response.xpath('//*[@id="footer-Social"]/div/ul/li[3]/a/@href').get(),
            "twitter": response.xpath('//*[@id="footer-Social"]/div/ul/li[2]/a/@href').get(),
            "youtube": response.xpath('//*[@id="footer-Social"]/div/ul/li[5]/a/@href').get(),
            "linkedin": response.xpath('//*[@id="footer-Social"]/div/ul/li[1]/a/@href').get(),
        }
        ranking = "not known"

        # Contact page URL
        contact_page_url = "https://www.umt.edu.pk/contact-us.aspx"
        yield scrapy.Request(
            url=contact_page_url,
            callback=self.parse_contact,
            meta={
                'university_title': university_title,
                'main_link': main_link,
                "social_links": social_links,
                'ranking': ranking,
                'introduction': introduction
            }
        )

    def parse_contact(self, response):
        # Extract contact details
        info_email = "info@ucp.du.pk"
        call_number = response.xpath('//*[@id="main"]/section[2]/div/div/div[2]/div/div/div[1]/div/p[2]/text()[2]').get()

        # Course page URL
        course_page_url = "https://admissions.umt.edu.pk/Search.aspx"
        yield scrapy.Request(
            url=course_page_url,
            callback=self.parse_course,
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

    def parse_course(self, response):
        # Extract course details
        courses = response.xpath('//div[@class="course-name"]/text()').getall()
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
           
        }
