import scrapy

class LumsSpider(scrapy.Spider):
    name = 'lums'
    allowed_domains = ['lums.edu.pk']
    start_urls = ['https://www.lums.edu.pk/']  # Add the starting URL for LUMS

    def parse(self, response):
        # Extract data for LUMS
        data = {
            'university_name': 'LUMS',
            'fee_structure': self.extract_fee_structure(response),
            'courses': self.extract_courses(response),
            'admission_dates': self.extract_admission_dates(response),
            'contact_info': self.extract_contact_info(response),
            'website': response.url
        }
        yield data
        
    def extract_fee_structure(self, response):
        # Code to extract fee structure data
        fee_structure = response.xpath('your-xpath-for-fee-structure').get()
        return fee_structure

    def extract_courses(self, response):
        # Code to extract available courses
        courses = response.xpath('your-xpath-for-courses').getall()
        return courses

    def extract_admission_dates(self, response):
        # Code to extract admission dates
        admission_dates = response.xpath('your-xpath-for-admission-dates').get()
        return admission_dates

    def extract_contact_info(self, response):
        # Code to extract contact information
        contact_info = response.xpath('your-xpath-for-contact-info').get()
        return contact_info
