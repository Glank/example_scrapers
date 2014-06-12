from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from BeautifulSoup import BeautifulSoup
import urllib2
import time
from simple_cache import Cache

MONMOUTH_CLASSES_PORTAL_URL = 'http://www2.monmouth.edu/muwebadv/wa3/search/SearchClasses.aspx'

#perform a classes search using selenium
def get_classes_page_html(term_number, subject_number):
    browser = webdriver.Firefox()
    browser.get(MONMOUTH_CLASSES_PORTAL_URL)
    session = browser.find_element_by_name('ddlTerm')
    for i in xrange(term_number):
        session.send_keys(Keys.ARROW_DOWN)
    subject = browser.find_element_by_name('ddlSubj_1')
    for i in xrange(subject_number):
        subject.send_keys(Keys.ARROW_DOWN)
    submit = browser.find_element_by_name('btnSubmit')
    submit.click()
    time.sleep(3)
    page_source = str(browser.page_source.encode('ascii', 'ignore'))
    browser.quit()
    return page_source
def get_cached_classes_page_html(term_number, subject_number):
    key = ("monmouth classes", term_number, subject_number)
    if key in Cache:
        return Cache[key]
    page_html = get_classes_page_html(term_number, subject_number)
    Cache[key] = page_html
    return page_html

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

def get_select_options(select_id, page_source):
    soup = BeautifulSoup(page_source)
    options = soup.find('select', {'id':select_id}).findAll("option")
    values = [str(elem["value"]) for elem in options if elem.has_key("value")]
    return values

def get_term_names():
    page_source = get_cached_page_html(MONMOUTH_CLASSES_PORTAL_URL)
    return get_select_options("ddlTerm", page_source)

def get_subject_names():
    page_source = get_cached_page_html(MONMOUTH_CLASSES_PORTAL_URL)
    return get_select_options("ddlSubj_1", page_source)

def get_class_info(term_number, subject_number):
    page_source = get_cached_classes_page_html(term_number, subject_number)
    soup = BeautifulSoup(page_source)
    table = soup.find('table', {'id':'dgdSearchResult'})
    rows = table.findAll('tr')
    class_info = []    
    for row in rows[1:]:
        cells = row.findAll('td')
        name = cells[0].a.span
        name = str(name.contents[0])+":"+str(name.contents[2])
        teacher = str(cells[2].contents[0])
        class_info.append((name,teacher))
    return class_info

def print_usage():
    print """
    Usage:
        python classes_scraper.py <term> <subject>
    """

if __name__=="__main__":
    import sys
    try:
        #parse the args
        term_names = get_term_names()
        term_number = term_names.index(sys.argv[1])
        subject_names = get_subject_names()
        subject_number = subject_names.index(sys.argv[2])

        #do the scrape
        for name, teacher in get_class_info(term_number, subject_number):    
            print teacher + ":\t" + name
    except Exception as e:
        print e
        print_usage()
    
