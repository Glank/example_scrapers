#Author: Ernest Kirstein

import re
from simple_cache import Cache
from BeautifulSoup import BeautifulSoup
import urllib2   

#retrieve pages
def get_page_html(page_url):
    response = urllib2.urlopen(page_url)
    html = response.read()
    return html
def get_cached_page_html(page_url):
    #either retrieve the page from the cache, 
    #or download the page and memoize it in the cache.
    if page_url in Cache:
        return Cache[page_url]
    page_html = get_page_html(page_url)
    Cache[page_url] = page_html
    return page_html

class Country:
    def __init__(self):
        self.name = None
        self.population = None
    def is_valid(self):
        if not re.match(r"[\(\)\w \-,]+$", self.name):
            return False
        if not isinstance(self.population, int):
            return False
        return True
    def __repr__(self):
        return self.name+": "+str(self.population)

def get_country(row):
    print row
    exit

def get_countries(source):
    soup = BeautifulSoup(source.decode("utf-8").encode("ascii", "ignore"))
    table = soup.find("table", {'class':'wikitable sortable'})
    rows = table.findAll("tr")
    countries = []
    for row in rows[1:]:
        cells = row.findAll("td")
        country = Country()
        country.name = str(cells[1].find('a').string)
        country.population = int("".join(re.findall('\d',str(cells[2].string))))
        if not country.is_valid():
            raise Exception(str(country))
        countries.append(country)
    return countries

if __name__=="__main__":
    url = "http://en.wikipedia.org/wiki/List_of_countries_by_population"
    source = get_cached_page_html(url)
    countries = get_countries(source)
    for country in countries:
        print country
