import scrapy
import json

class LCWUSpider(scrapy.Spider):
    name = "lcwu_spider"

    # Start with the URL of the university's main page or listing
    start_urls = ["https://www.lcwu.edu.pk/"]

    def parse(self, response):
        
        university_title = response.xpath('//title/text()').get().strip()
        
        # Main URL
        main_link = response.url
        contact=response.css("span.contact-telephone::text").get()
        camp=response.css("section#sp-bottom h5:nth-child(1)::text").get()
        
        # Extracting data as per the JSON format required
        university_data = [{
            "university_title": university_title,
            "main_link": main_link,
            "social_links": {
                "Youtube": "https://www.youtube.com/channel/UC6nOyKC6gx_IaXUYHZsnqyw",
                "facebook": "https://web.facebook.com/lcwu.official",
                "instagram": "null"
            },
            "ranking": "N/A",
            "contact_details": {
                "info_email": "registrar@lcwu.edu.pk",
                "call": contact
            },
            "introduction": "Welcome to Lahore College for Women University, one of the historic and the largest Women University in Asia. LCWU is a hub of academic excellence for women empowerment and entrepreneurship in Asia. This institute has played a pivotal role in empowering generations of women by providing quality higher education and has been contributing in the socio-economic development of the country since its inception.",
            "campuses": camp
        }]

        # Yield the data in JSON format
        yield university_data
        
        with open("lcwu.json", "w", encoding="utf-8") as f:
          json.dump(university_data, f, ensure_ascii=False, indent=2)
