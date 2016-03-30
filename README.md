# simple_scrapy
It is simple command line Linkedin scraper based on python scrapy library.
python 2.7+ or 3+

installation:
pip install scrapy

usage:
scrapy crawl linkedin -a login=your_linked_in_login -a password=your_linked_in_password -a search=Entwickler -o items.csv

where:
login and password: are from your linkedin account in order to login
search=Entwickler: word you are searching for
items.csv: resuling file (you can use .json as well)
