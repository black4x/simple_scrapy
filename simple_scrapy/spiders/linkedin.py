from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
import json
import re


class MySpider(InitSpider):
    name = 'lin'
    allowed_domains = ['linkedin.com']
    login_page = 'https://www.linkedin.com/uas/login'
    start_urls = ['https://www.linkedin.com/vsearch/f?type=all&keywords=fuhrparkleiter&orig=GLHD&rsid=&pageKey=oz-winner&trkInfo=tarId%3A1459209054521&search=Search']

    def init_request(self):
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        return FormRequest.from_response(response,
                                        formname='login',
                                        formdata={'session_key': 'a.juodel@gmail.com',
                                                   'session_password': 'XXX'},
                                        callback=self.check_login)

    def check_login(self, response):
        if "logout" in response.body:
            self.log("\n\n !!!! Login Success !!!!\n\n")
            return self.initialized()
        else:
            self.log("\n\n ****** ERROR\n\n")

    def parse(self, response):
        self.log("\n\nParsing: \n\n")


        regex = re.compile(r'<!--(.*)-->', re.DOTALL)
        comment = response.xpath("//code[@id='voltron_srp_main-content']/comment()").re(regex)[0].encode(encoding='UTF-8',errors='backslashreplace')

        vvv = re.sub(r'\\u002D', '-', comment, flags=re.IGNORECASE)
        json_dict = json.loads(vvv, encoding='UTF-8')

        r = json_dict['content']['page']['voltron_unified_search_json']['search']['results']
        for i in r:
            self.log(i['person']['fmt_location'])

        return []