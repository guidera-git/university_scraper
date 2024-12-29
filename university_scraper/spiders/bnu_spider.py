import scrapy

class BnuSpiderSpider(scrapy.Spider):
    name = "bnu_spider"
    allowed_domains = ["bnu.edu.pk"]
    start_urls = ["https://bnu.edu.pk"]

    def parse(self, response):
        # Hardcoded university title
        university_title = "BeaconHouse National University"
        
        # Extract the main link using the given XPath
        main_link = response.xpath('/html/body/div[1]/div[1]/div/div/div/div[1]/div[2]/a/@href').get()
        
        # Define social links (example: adjust XPaths as necessary)
        social_links = {
            "instagram_link": response.xpath('//a[contains(@href, "facebook.com")]/@href').get(),
            "facebook_link": response.xpath('//a[contains(@href, "instagram.com")]/@href').get(),
            "twitter_link": response.xpath('//a[contains(@href, "twitter.com")]/@href').get(),
            "dailymotion_link": response.xpath('//a[contains(@href, "dailymotion.com")]/@href').get(),
            "linkdin_link": response.xpath('//a[contains(@href, "linkedin.com")]/@href').get(),
        }

        # Yield the main page data and proceed to the "About Us" page
        yield scrapy.Request(
            url="https://www.bnu.edu.pk/about-us",
            callback=self.parse_about_us,
            meta={
                'university_title': university_title,
                'main_link': main_link,
                'social_links': social_links
            }
        )

    def parse_about_us(self, response):
        # Extract data from the "About Us" page
        about_us_content = response.xpath('/html/body/div[2]/div[1]/div/div/div[1]/div/p[1]/text()').getall()
        about_us_cleaned = " ".join(about_us_content).strip() if about_us_content else "No information found"
      
        # Extract contact details
        info_email = response.xpath('/html/body/section[1]/div/div/div[1]/div[2]/ul[1]/li[1]/a/text()').get()
        call_number = response.xpath('/html/body/section[1]/div/div/div[1]/div[2]/ul[1]/li[2]/a/text()').get()

        # Combine data from the previous request
        yield scrapy.Request(
            url="https://bnu.edu.pk/program/bsc-hons-in-computer-science",
            callback=self.parse_course_se,
            meta={
                  'university_title': response.meta['university_title'],
            'main_link': response.meta['main_link'],
            'social_links': response.meta['social_links'],
            'ranking': "not known",
            "contact_details": {
                "info_email": info_email,
                "call": call_number
            },
            'introduction': about_us_cleaned,
            }
        )
      

    def parse_course_se(self, response):
        program_title = response.xpath('/html/body/div[2]/div/div/div[2]/div/h2').get()
        program_description = response.xpath('//div[@id="section"]/div/p/text()').get()
        program_duration = response.xpath('/html/body/div[2]/div/div/div[2]/div/ul[1]/li[1]/p/text()').get()
        teaching_system = "Semester"
        session_begin = ""  # Adjust as needed
        credit_hours = response.xpath('/html/body/div[2]/div/div/div[2]/div/ul[1]/li[3]/p/text()').get()

        fee = "to be announced"  
        merit = "Not specified"

        admission_criteria = [
            {"s.no": 1, "criteria": response.xpath('//*[@id="pills-home"]/div/div[1]/div/ul/li[1]/text()').get()},
        ]

        course_outline = "https://bnu.edu.pk/program/bsc-hons-in-computer-science#courses"

        software_engineering = {
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

        yield scrapy.Request(
            url="https://bnu.edu.pk/program/bsc-hons-software-engineering",
            callback=self.parse_course_cs,
            meta = {
            "university_title": response.meta["university_title"],
            "main_link": response.meta["main_link"],
            "social_links": response.meta["social_links"],
            "contact_details": response.meta["contact_details"],
            "introduction": response.meta["introduction"],
            "programs": {
                "software_engineering": software_engineering
            }
            }
        )

    def parse_course_cs(self, response):
        program_title = response.xpath('/html/body/div[2]/div/div/div[2]/div/h2').get()
        program_description = response.xpath('//*[@id="section"]/div/p/text()').get()
        program_duration = response.xpath('/html/body/div[2]/div/div/div[2]/div/ul[1]/li[1]/p/text()').get()
        teaching_system = "Semester"
        session_begin = ""  # Adjust as needed
        credit_hours = response.xpath('/html/body/div[2]/div/div/div[2]/div/ul[1]/li[3]/p/text()').get()

        fee = "to be announced"  
        merit = "Not specified"

        admission_criteria = [
            {"s.no": 1, "criteria": response.xpath('//*[@id="pills-home"]/div/div[1]/div/ul/li[1]/text()').get()},
        ]

        course_outline = "https://bnu.edu.pk/program/bsc-hons-software-engineering"

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
        
        campuses= "Lahore"
        yield{
         "university_title": response.meta["university_title"],
            "main_link": response.meta["main_link"],
            "social_links": response.meta["social_links"],
            "contact_details": response.meta["contact_details"],
            "introduction": response.meta["introduction"],
            "programs": {
                "software_engineering": response.meta["programs"]["software_engineering"],
                "computer science": computer_science
            },
            "campuses": campuses
    }


