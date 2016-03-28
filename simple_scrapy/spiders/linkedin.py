from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest

class MySpider(InitSpider):
    name = 'lin'
    allowed_domains = ['linkedin.com']
    login_page = 'https://www.linkedin.com/uas/login'
    start_urls = ['https://www.linkedin.com/vsearch/p?type=people&keywords=%22fuhrparkleiter%22']

    login = ''
    password = ''


    def init_request(self):
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        return FormRequest.from_response(response,
                                        formname='login',
                                        formdata={'session_key': login,
                                                   'session_password': password},
                                        callback=self.check_login)

    def check_login(self, response):
        if "logout" in response.body:
            self.log("\n\n !!!! Login Success !!!!\n\n")
            return self.initialized()
        else:
            self.log("\n\n ****** ERROR\n\n")

    def parse(self, response):
        self.log("\n\nParse begins \n\n")
        return []