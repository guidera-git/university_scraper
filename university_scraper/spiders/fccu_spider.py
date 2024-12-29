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
        
        # Make a request to the Computer Science program page
        yield scrapy.Request(
            url="https://www.fccollege.edu.pk/baccalaureate-in-computer-sciences/",
            callback=self.parse_course_cs,
            meta = {
                'university_title': university_title,
                'main_link': main_link,
                'social_links': social_links,
                'ranking': ranking,
                "contact_details": {
                    'info_email': info_email,
                    'call': call_number
                },
                'introduction': introduction,
            })

    def parse_course_cs(self, response):
        # Extracting course information from the Computer Science program page
        program_title = response.xpath('//*[@id="post-6014"]/div/div[1]/div/div/div/div[1]/h2/text()').get()  # Adjust the XPath as needed
        program_description = response.xpath('//*[@id="tab-bde53d4c82502f71624"]/p/span[2]/text()').get()  # Adjust the XPath as needed
        program_duration = "4years"
        credit_hours = "not known"
        fee ="337000 per semester" 
        merit = "not known"
        teaching_system = "Semester"
        session_begin = ""
        admission_criteria = [
            {"s.no": 1, "criteria": response.xpath('//*[@id="tab-ca551c2baf392c6dc08"]/p[1]/text()').get()},
            {"s.no": 2, "criteria": response.xpath('//*[@id="tab-ca551c2baf392c6dc08"]/p[2]/text()').get()},
            {"s.no": 3, "criteria": response.xpath('//*[@id="tab-ca551c2baf392c6dc08"]/p[2]/text()[3]').get()},
            {"s.no": 4, "criteria": response.xpath('//*[@id="tab-ca551c2baf392c6dc08"]/p[2]/text()[5]').get()},
            {"s.no": 5, "criteria": response.xpath('//*[@id="tab-ca551c2baf392c6dc08"]/p[2]/text()[7]').get()},
            {"s.no": 6, "criteria": response.xpath('//*[@id="tab-ca551c2baf392c6dc08"]/p[2]/text()[8]').get()},
        ]  
        course_outline = "https://www.fccollege.edu.pk/baccalaureate-in-computer-sciences/"
        # Store the extracted data in a structured format
        computer_science = {
            "program_title": program_title,
            "program_description": program_description,
            "program_duration": program_duration,
            "credit_hours": credit_hours,
            "fee": fee,
            "merit": merit,
            "teaching_system": teaching_system,
            "session_begin": session_begin,
            "admission_criteria": admission_criteria,
            "course_outline": course_outline
        }

        # Yield the final scraped data
        yield {
            'university_title': response.meta['university_title'],
            'main_link': response.meta['main_link'],
            'social_links': response.meta['social_links'],
            'ranking': response.meta['ranking'],
            "contact_details": response.meta['contact_details'],
            'introduction': response.meta['introduction'],
            "programs": {
                "computer science": computer_science
            },
            "campuses": "Lahore"
        }
