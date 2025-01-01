import scrapy
import json
class UOESpider(scrapy.Spider):
    name = "uoe_spider"
    allowed_domains = ["ue.edu.pk"]
    start_urls = ["https://ue.edu.pk/"]

    def parse(self, response):  # Corrected method name
        # Extracting the university title
        university_title = response.xpath('//title/text()').get().strip()
        
        # Main URL
        main_link = response.url
        
        # Social links
        social_links = response.css("ul.ueitcell-social-icons li a::attr(href)").getall()
        social_links_dict = {
            "facebook": next((link for link in social_links if "facebook" in link), ""),
            "twitter": next((link for link in social_links if "twitter" in link), ""),
            "instagram": next((link for link in social_links if "instagram" in link), ""),
            "youtube": next((link for link in social_links if "youtube" in link), ""),
            "linkedin": next((link for link in social_links if "linkedin" in link), ""),
        }
        
        # Contact details (adjust selectors based on actual HTML structure)
        intro = response.css("div.col-md-3.ueitcell-widget p:nth-child(2)::text").get()
        
        email = response.css("div.col-md-3.ueitcell-widget p:nth-child(1)::text").get()
        phone = response.css("div.col-md-3.ueitcell-widget p:nth-child(3)::text").get()
        
        # Final result dictionary
        result = {
            "university_title": university_title,
            "main_link": main_link,
            "social_links": social_links_dict,
            "ranking": "N/A",  # Replace with actual ranking if available
            "contact_details": {
                "email": email,
                "phone": phone,
            },
            "introduction": intro,
            "programs": [],
        }
        
        # Yielding the result
        yield result
         
        with open("uoe.json", "w", encoding="utf-8") as f:
          json.dump(result, f, ensure_ascii=False, indent=2)