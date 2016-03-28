import scrapy


class LinkedinSpider(scrapy.Spider):
    name = "linkedin"
    allowed_domains = ["https://www.linkedin.com"]
    start_urls = [
        "https://www.linkedin.com/vsearch/p?type=people&keywords=%22fuhrparkleiter%22",
    ]

    def parse(self, response):
        pass