# simple_scrapy
It is simple command line Linkedin scraper based on python scrapy library.
<br>python 2.7+ or 3+

<h5>installation:</h5>
pip install scrapy

<h5>usage:</h5>
scrapy crawl linkedin -a login=your_login -a password=your_password -a search=Entwickler -o items.csv

where:
<ul>
<li>login and password: your linkedin account</li>
<li>search=Entwickler: word you are searching for</li>
<li>items.csv: resuling file (you can use .json as well)</li>
</ul>
