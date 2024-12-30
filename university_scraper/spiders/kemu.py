import scrapy

class KEMUpider(scrapy.Spider):
    name = "kemu_spider"
    start_urls = ["https://kemu.edu.pk/"]

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
        main_link = response.xpath('//*[@id="wrapper"]/div[2]/div[2]/div/div[1]/div/div/span/a/img').get()

        social_links = {
            "instagram": response.xpath('//*[@id="wrapper"]/div[4]/div/div/div[2]/div[2]/div/div[2]/div/div/a[3]').get(),
            "facebook": response.xpath('//*[@id="wrapper"]/div[4]/div/div/div[2]/div[2]/div/div[2]/div/div/a[1]').get(),
            "twitter": response.xpath('//*[@id="wrapper"]/div[4]/div/div/div[2]/div[2]/div/div[2]/div/div/a[2]').get(),
        }


def MBBS(self, response):
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