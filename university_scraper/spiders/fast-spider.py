import scrapy
import json
import re


class FastSpider(scrapy.Spider):
    name = "fast-spider"
    allowed_domains = ["nu.edu.pk"]
    start_urls = ["https://www.nu.edu.pk/"]
    valid_programs = [
        "Bachelor of Science (Computer Science)", "Bachelor of Science (Software Engineering)", "Bachelor of Science (Cyber Security)",
        "Bachelor of Science (Data Science)", "Bachelor of Science (Artificial Intelligence)",
        "Bachelor of Science (Electrical Engineering)", "Bachelor of Science (Civil Engineering)",
        "BS Chemical Engineering", "Bachelor of Science (Computer Engineering)"
    ]
    fee_structure_url = "https://www.nu.edu.pk/Admissions/FeeStructure"

    def parse(self, response):
        # Extract university title and main link
        university_title = response.xpath('//title/text()').get(default="Unknown Title").strip()
        main_link = response.url

        # Extract all social links
        social_links = response.css("li.socials a::attr(href)").getall()
        intro_text = response.xpath("//div[@class='col-md-12']//p[@class='text-justify']/text()").getall()
        cleaned_intro = " ".join([re.sub(r'\s+', ' ', para.strip()) for para in intro_text])

        # Map links to their respective platforms
        social_links_dict = {
            "facebook": next((link for link in social_links if "facebook" in link), ""),
            "twitter": next((link for link in social_links if "twitter" in link), ""),
            "instagram": next((link for link in social_links if "instagram" in link), ""),
            "youtube": next((link for link in social_links if "youtube" in link), ""),
        }

        contact_phone = response.css("ul.col-md-6.col-sm-6.list-unstyled li a.padding-left-15::text").get(default="N/A")

        # Extract campus names and URLs
        all_names = response.css(
            "ul.nav-links li:nth-child(3) ul li.dropdown.menu-item.dropdown-submenu a.link-page::text"
        ).getall()
        campus_names = [name.strip() for name in all_names if "campus" in name.lower()]
        campus_urls = response.css(
            "ul.nav-links li:nth-child(3) ul li.dropdown.menu-item.dropdown-submenu ul.dropdown-menu.edugate-dropdown-menu-2 li:nth-child(1).menu-item a.link-page::attr(href)"
        ).getall()

        campuses = {}
        for campus_name, campus_url in zip(campus_names, campus_urls):
            campuses[campus_name] = response.urljoin(campus_url)

        # Add additional information
        result = [{
            "university_title": university_title,
            "main_link": main_link,
            "social_links": social_links_dict,
            "ranking": "4",  # Example ranking
            "contact_details": {"call": contact_phone},
            "introduction": cleaned_intro,
            "programs": {},
            "campuses": campuses,
        }]

        # Navigate to the fee structure page
        yield scrapy.Request(
            url=self.fee_structure_url,
            callback=self.parse_fee_structure,
            meta={"result": result},
        )

    def parse_fee_structure(self, response):
        # Extract tuition fee per credit hour
        fee_table = response.css(
            "div.table-responsive table.edu-table-responsive.table-bordered.table-condensed.table-hover.table-striped tbody.table-body"
        )
        fee_row = fee_table.css("tr")
        tuition_fee_per_credit = 10000  # Default fee

        if fee_row:
            fee_text = fee_row.css("td.text-center::text").get()
            if fee_text:
                fee_text = fee_text.replace("Rs.", "").replace(",", "").strip()
                tuition_fee_per_credit = int(fee_text)

        result = response.meta.get("result", {})

        # Navigate to the degree programs page
        degree_programs_url = "https://www.nu.edu.pk/Degree-Programs"
        yield scrapy.Request(
            url=degree_programs_url,
            callback=self.parse_degree_programs,
            meta={"result": result, "tuition_fee_per_credit": tuition_fee_per_credit},
        )

    def parse_degree_programs(self, response):
        result = response.meta.get("result", {})
        tuition_fee_per_credit = response.meta.get("tuition_fee_per_credit", 10000)

        programs_table = response.css("tbody.table-body")
        degree_rows = programs_table.css("tr")[1:13]

        for row in degree_rows:
            degree_name = row.css("td.custom-width1 a::text").get(default="Unknown Program").strip()
            degree_link = response.urljoin(row.css("td.custom-width1 a::attr(href)").get(default=""))

            if degree_name in self.valid_programs:
                self.logger.info(f"Valid program: {degree_name}")
                yield response.follow(
                    degree_link,
                    callback=self.parse_degree,
                    meta={
                        "result": result,
                        "degree_name": degree_name,
                        "degree_url": degree_link,
                        "tuition_fee_per_credit": tuition_fee_per_credit,
                    },
                )

    def parse_degree(self, response):
        result = response.meta.get("result", {})
        degree_name = response.meta.get("degree_name", "Unknown Degree")
        tuition_fee_per_credit = response.meta.get("tuition_fee_per_credit", 10000)
        description = " ".join(
            [para.strip() for para in response.xpath("//div[@class='text-justify']//p//text()").getall()]
        )

        # Extract merit formula and admission criteria
        admission_criteria, merit_formula = self.extract_admission_and_merit_criteria(response,degree_name)
        # Structure for degree details
        degree_details = {
            "program_title": degree_name,
            "program_description": description,
            "program_duration": "4 years",  # Default duration, to be updated later
            "credit_hours": "130",  # Default credit hours, to be updated later
            "fee": [
                {
                    "per_credit_hour_fee": tuition_fee_per_credit,
                    "total_tution_fee": "N/A"  # To be calculated later
                }
            ],
            "important_dates": [],  # Leave empty if no data is available
            "merit": merit_formula,  # Extracted merit formula
            "admission_criteria": admission_criteria,  # Extracted admission criteria
            "merit_formula": merit_formula,  # Add merit formula as a separate field
            "course_url": response.url  # Example URL, modify as needed
        }

        total_program_credits = 0
        total_program_fees = 0
        total_semesters = 0
        semesters = response.css("div.col-md-12 div.col-md-6.margin-bottom-10")

        for semester_index, semester in enumerate(semesters):
            semester_name = semester.css("tr.heading-content td h5.text-white.no-margin::text").get(default="Semester")
            semester_fee = 0
            semester_total_credits = 0
            total_semesters += 1

            courses = semester.css("tr.table-row")
            for course in courses:
                course_name = course.css("td.text-left.padding-left-20::text").get(default="Unknown Course")
                credit_hours_text = course.css("td.text-center::text")[1].get()
                credit_hours = sum(map(int, credit_hours_text.split("+"))) if credit_hours_text else 0

                course_fee = credit_hours * tuition_fee_per_credit
                semester_fee += course_fee
                semester_total_credits += credit_hours

            semester_fee += 2500  # Student activities fund
            if semester_index == 0:
                semester_fee += 30000 + 20000

            total_program_credits += semester_total_credits
            total_program_fees += semester_fee

        # Calculate program duration based on semesters (2 semesters = 1 year)
        program_duration_years = total_semesters // 2
        degree_details["program_duration"] = f"{program_duration_years} years"
        degree_details["credit_hours"] = total_program_credits
        degree_details["fee"][0]["total_tution_fee"] = f"{total_program_fees} PKR"

        # Add the degree to the results
        result[0]["programs"][degree_name.lower().replace(" ", "_")] = degree_details

        # Save data to JSON
        with open("new.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        self.log(f"Data saved for degree: {degree_name}")
        
    def extract_admission_and_merit_criteria(self, response, degree_name):
        admission_criteria = []
        merit_formula = []

    # List of keywords related to computer programs
        computer_keywords = [
            "computer", "software", "data science", "cyber security", "artificial intelligence"
        ]
    
    # Check if degree_name contains any of the computer-related keywords
        if any(keyword.lower() in degree_name.lower() for keyword in computer_keywords):
            program_type = "computer"
        else:
            program_type = "engineering"

        self.logger.info(f"Program type for {degree_name}: {program_type}")
        # self.logger.info(f"Panels found: {len(panels)}")

        if program_type == "engineering":
        # For Engineering programs, extract the first panel
            engineering_panel = response.xpath("//div[@class='panel'][1]") 
            self.logger.info("Extracting criteria and merit for engineering program.")
            admission_criteria += self.parse_panel_criteria_and_merit(engineering_panel, program_type="engineering")

        if program_type == "computer":
        # For Computer programs, extract the second panel
            computing_panel = response.xpath("//div[@class='panel'][2]")
            self.logger.info("Extracting criteria and merit for computer program.")
            admission_criteria += self.parse_panel_criteria_and_merit(computing_panel, program_type="computer")

        return admission_criteria, merit_formula



    def parse_panel_criteria_and_merit(self, panel, program_type):
        admission_criteria = []
        merit_formula = []
        
    # Extract program type (heading)
        

    # Parse the admission criteria (first 6 tr tags)
        criteria_rows = panel.xpath("//div[@id='collapse-1-1']//table/tbody/tr[position()<=6]")
        
        for idx, row in enumerate(criteria_rows, start=1):
            criteria_text = row.xpath("//td/p/span/text()").get()
            self.logger.info(f"Criteria {idx}: {criteria_text}")
            admission_criteria.append({
            "s.no": idx,
            "criteria": criteria_text.strip() if criteria_text else "No criteria found"
    })

    # Parse the merit formula (last 3 tr tags)
        formula_rows = panel.xpath("//div[@id='collapse-1-1']//table/tbody/tr[position() >= 7 and position() <= 9]")
        for row in formula_rows:
            metric = row.xpath("//td//b//text()").get()
            value = row.xpath("//td[2]//text()").get()
            merit_formula.append({
            metric.strip() if metric else "No metric": value.strip() if value else "No value"
        })

        return admission_criteria, merit_formula