import scrapy

class UniversityScraperItem(scrapy.Item):
    university_title = scrapy.Field()
    main_link = scrapy.Field()
    social_links = scrapy.Field()
    ranking = scrapy.Field()
    contact_details = scrapy.Field()
    introduction = scrapy.Field()
    programs = scrapy.Field()
    campuses = scrapy.Field()
