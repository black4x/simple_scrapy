from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
import json
import re

from simple_scrapy.items import PersonItem


class MySpider(InitSpider):
    name = 'lin'
    allowed_domains = ['linkedin.com']
    login_page = 'https://www.linkedin.com/uas/login'
    start_urls = ['https://www.linkedin.com/vsearch/f?type=people&keywords=fuhrparkleiter']

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

    def create_person_item(self, person):
        item = PersonItem()
        first_name = 'firstName'
        last_name = 'lastName'
        if first_name in person:
            item[first_name] = person[first_name]
        if last_name in person:
            item[last_name] = person[last_name]
        try:
            item['city'], item['country'] = [x.strip() for x in person['fmt_location'].split(',')]
        except:
            item['city'], item['country'] = person['fmt_location'], None
        return item


    def parse(self, response):
        self.log("\n\nParsing: \n\n")

        regex = re.compile(r'<!--(.*)-->', re.DOTALL)
        comment = response.xpath("//code[@id='voltron_srp_main-content']/comment()").re(regex)[0].encode(encoding='UTF-8',errors='backslashreplace')
        vvv = re.sub(r'\\u002D', '-', comment, flags=re.IGNORECASE)
        json_dict = json.loads(vvv, encoding='UTF-8')

        results = json_dict['content']['page']['voltron_unified_search_json']['search']['results']

        for res_array in results:
            yield self.create_person_item(res_array['person'])
