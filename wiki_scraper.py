#Author: Ernest Kirstein

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
        if not re.match("[\w ]+$", self.name):
            return False
        if not isinstance(self.population, int):
            return False
        return True

def get_country(row):
    print row
    exit

def get_countries(source):
    soup = BeautifulSoup(source)
    print soup.findAll("table", {"wikitable sortable jquery-tablesorter"})

if __name__=="__main__":
    url = "http://en.wikipedia.org/wiki/List_of_countries_by_population"
    source = get_cached_page_html(url)
    print source
