from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
import json
import re

from simple_scrapy.items import PersonItem


class MySpider(InitSpider):
    name = 'linkedin'
    allowed_domains = ['linkedin.com']
    login_page = 'https://www.linkedin.com/uas/login'

    def __init__(self, login='', password='', search="fuhrparkleiter"):
        """params from command line
        """
        #search URL
        self.start_urls = ['https://www.linkedin.com/vsearch/f?type=people&keywords=%s' % search]
        self.login = login
        self.password = password

    def init_request(self):
        """ first entry point, going to login page
        """
        return Request(url=self.login_page, callback=self.go_login)

    def go_login(self, response):
        """describe login form
            after submit redirect to check_login
        """
        return FormRequest.from_response(response,
                                        formname='login',
                                        formdata={'session_key': self.login,
                                                   'session_password': self.password},
                                        callback=self.check_login)

    def check_login(self, response):
        """checking if login successful
        """
        if "logout" in response.body:
            self.log("\n\n !!!! Login Success !!!!\n\n")
            return self.initialized()
        else:
            self.log("\n\n ****** Login ERROR\n\n")

    def create_person_item(self, person):
        """create person item by extracting data from json ..[results][person]
        """
        item = PersonItem()
        try:
            first_name = 'firstName'
            last_name = 'lastName'
            item[first_name] = person[first_name] if first_name in person else None
            item[last_name] = person[last_name] if last_name in person else None
            # finding city and country using ','
            city_country = person['fmt_location'].split(',')
            try:
                item['city'] = city_country[0].strip()
                item['country'] = city_country[1].strip()
            except IndexError as e:
                self.log(e)
            # finding current position and company using: bei, at
            pos_company = re.split(r'bei|at', person["fmt_headline"])
            try:
                item['position'] = re.sub(r'<B>|</B>','', pos_company[0])
                item['company'] = pos_company[1]
            except IndexError as e:
                self.log(e)
        #preventing spot execution if one item has problem
        except Exception as e:
            self.log(e)
        return item

    def parse(self, response):
        """main parsing method, starts after self.initialized() call
        """
        # reqular expression to get json from comment
        regex = re.compile(r'<!--(.*)-->', re.DOTALL)
        commented_json = response.xpath("//code[@id='voltron_srp_main-content']/comment()").re(regex)[0].encode(
            encoding='UTF-8',
            errors='backslashreplace')
        # clearing json from unalloyed symbol
        commented_json = re.sub(r'\\u002D', '-', commented_json, flags=re.IGNORECASE)
        # parsing json
        json_dict = json.loads(commented_json, encoding='UTF-8')
        # navigating to results section
        results = json_dict['content']['page']['voltron_unified_search_json']['search']['results']
        # yield each Item
        for res_array in results:
            if 'person' in res_array:
                yield self.create_person_item(res_array['person'])
