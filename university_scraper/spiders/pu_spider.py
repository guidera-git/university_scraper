import scrapy

class PUSpider(scrapy.Spider):
    name = "pu_spider"
    start_urls = ["https://pu.edu.pk/page"]

    def parse(self, response):
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

        social_links = {
            "instagram": response.xpath('//*[@id="header"]/div[2]/div[1]/ul/li[4]/a/@href').get(),
            "facebook": response.xpath('//*[@id="header"]/div[2]/div[1]/ul/li[2]/a/@href').get(),
            "twitter": response.xpath('//*[@id="header"]/div[2]/div[1]/ul/li[3]/a/@href').get(),
        }

        ranking = "3"

        software_engineering_url = "https://pu.edu.pk/program/show/900079/Department-of-Software-Engineering"
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
        program_title = response.xpath('//*[@id="news-blocks"]/section/div/div[2]/div/h1/text()').get().strip()
        program_description = "The BS Software Engineering program aims to produce graduates with a strong foundation in computing, capable of applying theoretical concepts to solve problems, using appropriate methodologies and tools for software design and testing. Graduates are well-prepared for careers in the IT industry, graduate studies, and lifelong learning, with strong communication skills."

        program_duration = response.xpath("//div[contains(@class, 'block') and contains(text(), 'year')]/text()").get()
        if program_duration:
            program_duration = program_duration.strip()  
            program_duration = " ".join(program_duration.split())
        else:
            program_duration = "Not available" 

        teaching_system = response.xpath("//div[contains(@class, 'block') and contains(text(), 'System')]/text()").get()
        if teaching_system:
            teaching_system = teaching_system.strip()  
            teaching_system = " ".join(teaching_system.split())  
        else:
            teaching_system = "Not available"

        session_begin = response.xpath("//div[contains(@class, 'block') and contains(text(), 'er')]/text()").get()
        if session_begin:
            session_begin = session_begin.strip()  
            session_begin = " ".join(session_begin.split())  
        else:
            session_begin = "Not available"

        credit_hours = response.xpath("//div[contains(@class, 'block') and contains(text(), '1')]/text()").get()
        if credit_hours:
            credit_hours = credit_hours.strip()  
            credit_hours = " ".join(credit_hours.split())  
        else:
            session_begin = "Not available"

        fee = "90,000 PKR"

        merit= "89.23%"


        course_outline = [
        {"course_name": "Introduction to Computing", "semester": "1st Semester", "credit_hours": 3},
        {"course_name": "Calculus I", "semester": "1st Semester", "credit_hours": 3},
        {"course_name": "Mechanics and Wave Motion", "semester": "1st Semester", "credit_hours": 3},
        {"course_name": "Writing Workshop", "semester": "1st Semester", "credit_hours": 3},
        {"course_name": "Islamic Studies I", "semester": "1st Semester", "credit_hours": 2},
        {"course_name": "Programming Fundamentals", "semester": "2nd Semester", "credit_hours": 3},
        {"course_name": "Digital Logic Design", "semester": "2nd Semester", "credit_hours": 3},
        {"course_name": "Digital Logic Design Lab", "semester": "2nd Semester", "credit_hours": 1},
        {"course_name": "Calculus II", "semester": "2nd Semester", "credit_hours": 3},
        {"course_name": "Electricity and Magnetism", "semester": "2nd Semester", "credit_hours": 3},
        {"course_name": "Social Science Elective", "semester": "2nd Semester", "credit_hours": 3},
        {"course_name": "Discrete Mathematics", "semester": "3rd Semester", "credit_hours": 4},
        {"course_name": "Object Oriented Programming", "semester": "3rd Semester", "credit_hours": 3},
        {"course_name": "Comp Org and Assembly Lang", "semester": "3rd Semester", "credit_hours": 3},
        {"course_name": "Comp Org and Assembly Lang Lab", "semester": "3rd Semester", "credit_hours": 1},
        {"course_name": "Communication Skills", "semester": "3rd Semester", "credit_hours": 3},
        {"course_name": "Arabic Language", "semester": "3rd Semester", "credit_hours": 3},
        {"course_name": "Data Structures and Algorithms", "semester": "4th Semester", "credit_hours": 3},
        {"course_name": "Software Engineering", "semester": "4th Semester", "credit_hours": 3},
        {"course_name": "Linear Algebra", "semester": "4th Semester", "credit_hours": 3},
        {"course_name": "Probability and Statistics", "semester": "4th Semester", "credit_hours": 3},
        {"course_name": "Technical and Business Writing", "semester": "4th Semester", "credit_hours": 3},
        {"course_name": "Islamic Studies II", "semester": "4th Semester", "credit_hours": 2},
        {"course_name": "Operating Systems", "semester": "5th Semester", "credit_hours": 3},
        {"course_name": "Database Systems", "semester": "5th Semester", "credit_hours": 3},
        {"course_name": "OO Analysis and Design", "semester": "5th Semester", "credit_hours": 3},
        {"course_name": "Analysis of Algorithm", "semester": "5th Semester", "credit_hours": 3},
        {"course_name": "Software Requirements Engineering", "semester": "5th Semester", "credit_hours": 3},
        {"course_name": "Humanities Elective", "semester": "5th Semester", "credit_hours": 3},
        {"course_name": "Computer Networks", "semester": "6th Semester", "credit_hours": 3},
        {"course_name": "Computer Networks Lab", "semester": "6th Semester", "credit_hours": 1},
        {"course_name": "Software Design and Architecture", "semester": "6th Semester", "credit_hours": 3},
        {"course_name": "Enterprise System Development", "semester": "6th Semester", "credit_hours": 3},
        {"course_name": "Technical Elective", "semester": "6th Semester", "credit_hours": 3},
        {"course_name": "Pakistan Studies", "semester": "6th Semester", "credit_hours": 2},
        {"course_name": "Social Science Elective", "semester": "6th Semester", "credit_hours": 3},
        {"course_name": "Capstone Project I", "semester": "7th Semester", "credit_hours": 3},
        {"course_name": "Software Project Management", "semester": "7th Semester", "credit_hours": 3},
        {"course_name": "Software Quality Assurance", "semester": "7th Semester", "credit_hours": 3},
        {"course_name": "Human Computer Interaction", "semester": "7th Semester", "credit_hours": 3},
        {"course_name": "Humanities Elective", "semester": "7th Semester", "credit_hours": 3},
        {"course_name": "Capstone Project II", "semester": "8th Semester", "credit_hours": 3},
        {"course_name": "Technical Elective", "semester": "8th Semester", "credit_hours": 3},
        {"course_name": "Technical Elective", "semester": "8th Semester", "credit_hours": 3},
        {"course_name": "Technical Elective", "semester": "8th Semester", "credit_hours": 3},
        {"course_name": "Social Science Elective", "semester": "8th Semester", "credit_hours": 3}
    ]
        admission_criteria= [   
        {"s.no": 1, "criteria": "Intermediate of Computer Science (ICS) with at least 50% obtained marks"},
        {"s.no": 2, "criteria": "F.Sc. Pre-Engineering with at least 50% obtained marks"},
        {"s.no": 3, "criteria": "Intermediate with Mathematics & Physics with atleast 50% obtained marks"},
        {"s.no": 4, "criteria": "Intermediate with Mathematics & Computer Science with atleast 50% obtained marks"},
        {"s.no": 5, "criteria": "Intermediate with Mathematics & Statistics with atleast 50% obtained marks"},
        {"s.no": 6, "criteria": "F.Sc. Pre-Medical with additional Math with atleast 50% obtained marks"},
        {"s.no": 7, "criteria": "F.Sc. Pre-Medical with atleast 50% obtained marks"},
        {"s.no": 8, "criteria": "At least 60% marks in DAE in a relevant discipline."},
        {"s.no": 9, "criteria": "A-Levels (with equivalence of mentioned above by IBCC) with at least 50% obtained marks"}
        ]

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
            "course_outline": course_outline  # Store the extracted table data
        }

        contact_page_url = "https://pu.edu.pk/page/show/contact-us.html"
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
        info_email = response.xpath('//*[@id="ntb"]/tbody/tr[7]/td[1]/span/span/font/a/font/text()').get()
        call_number = response.xpath('//*[@id="ntb"]/tbody/tr[6]/td[2]/span/span/font/font/text()').get()

        campuses_page_url = "https://pu.edu.pk/page/show/Campuses.html"
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
            "new_campus": response.xpath('//table//tr[2]/td[1]/a/@href').get(),
            "old_campus": response.xpath('//table//tr[2]/td[3]/a/@href').get(),
            "gujranwala_campus": response.xpath('//table//tr[3]/td[1]/a/@href').get(),
            "khanspur_campus": response.xpath('//table//tr[3]/td[3]/a/@href').get(),
            "jhelum_campus": response.xpath('//table//tr[4]/td[1]/div/a/@href').get(),
            "pothohar_campus": response.xpath('//table/tbody/tr[4]/td[3]/div/a/@href').get()
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
            "programs":{ "software_engineering":response.meta["software_engineering"]
            } ,
            "campuses": campus_links
        }
