import scrapy

class LUMSSpider(scrapy.Spider):
    name = "lums_spider"
    start_urls = ["https://www.lums.edu.pk/"]

    def parse(self, response):
        descriptions = response.css('div.field--name-field-description div.field--item::text').getall()
        full_description = " ".join(descriptions).strip()

        homepage_url = "https://www.lums.edu.pk/"
        yield scrapy.Request(
            url=homepage_url,
            callback=self.parse_homepage,
            meta={"introduction": full_description}
        )

    def parse_homepage(self, response):
        university_title = response.css('title::text').get().strip()
        main_link = "https://www.lums.edu.pk/"

        social_links = {
            "instagram": response.css('ul.social-icons a[href*="instagram"]::attr(href)').get(),
            "facebook": response.css('ul.social-icons a[href*="facebook"]::attr(href)').get(),
            "twitter": response.css('ul.social-icons a[href*="twitter"]::attr(href)').get(),
        }

        ranking = "Top 1 in Pakistan for Business Education"  # Adjust this as needed

        software_engineering_url = "https://lums.edu.pk/academics/schools/school-science-engineering/undergraduate-programs/software-engineering"
        yield scrapy.Request(
            url=software_engineering_url,
            callback=self.parse_software_engineering,
            meta={
                "university_title": university_title,
                "main_link": main_link,
                "social_links": social_links,
                "ranking": ranking,
                "introduction": response.meta["introduction"]
            }
        )

    def parse_software_engineering(self, response):
        program_title = response.css('h1.page-title::text').get().strip()
        program_description = "The Software Engineering program at LUMS prepares students to design and develop software solutions, with a solid foundation in computer science, engineering, and problem-solving methodologies."

        program_duration = "4 years"
        teaching_system = response.css('div.teaching-methodology::text').get()
        session_begin = "Fall 2024"  # Adjust as needed
        credit_hours = "132 credits"  # Adjust based on the program data

        fee = "Approx. 1,200,000 PKR per year"  # Adjust based on the program data
        merit = "Not specified"

        admission_criteria = [
            {"s.no": 1, "criteria": "A-Levels or equivalent with at least 50% marks"},
            {"s.no": 2, "criteria": "Intermediate (Pre-Engineering) with at least 50% marks"},
            {"s.no": 3, "criteria": "Intermediate (Pre-Medical) with additional Math or Computer Science with at least 50% marks"},
            {"s.no": 4, "criteria": "At least 60% marks in DAE in a relevant discipline."},
            {"s.no": 5, "criteria": "SAT or GRE scores may also be considered."},
        ]

        course_outline = "https://lums.edu.pk/academics/schools/school-science-engineering/undergraduate-programs/software-engineering"
        
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

        contact_page_url = "https://www.lums.edu.pk/contact-us"
        yield scrapy.Request(
            url=contact_page_url,
            callback=self.parse_contact,
            meta={
                "university_title": response.meta["university_title"],
                "main_link": response.meta["main_link"],
                "social_links": response.meta["social_links"],
                "ranking": response.meta["ranking"],
                "introduction": response.meta["introduction"],
                "software_engineering": software_engineering
            }
        )

    def parse_contact(self, response):
        info_email = response.css('a[href^="mailto:"]::attr(href)').get()
        call_number = response.css('div.phone-number::text').get()

        campuses_page_url = "https://www.lums.edu.pk/our-campus"
        yield scrapy.Request(
            url=campuses_page_url,
            callback=self.parse_campuses,
            meta={
                "university_title": response.meta["university_title"],
                "main_link": response.meta["main_link"],
                "social_links": response.meta["social_links"],
                "ranking": response.meta["ranking"],
                "introduction": response.meta["introduction"],
                "software_engineering": response.meta["software_engineering"],
                "info_email": info_email,
                "call_number": call_number
            }
        )

    def parse_campuses(self, response):
        campus_links = {
            "main_campus": response.css('a[href*="campus"]::attr(href)').get(),
            "remote_campus": response.css('a[href*="remote-campus"]::attr(href)').get(),
        }

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
            "programs": {
                "software_engineering": response.meta["software_engineering"]
            },
            "campuses": campus_links
        }
