#Author: Ernest Kirstein

from BeautifulSoup import BeautifulSoup
import urllib2   

#retrieve pages
def get_page_html(page_url):
    response = urllib2.urlopen(page_url)
    html = response.read()
    return html

def get_front_page_article_urls():
    #get the front page html and put it through BeautifulSoup
    html = get_page_html("http://en.chessbase.com/")
    soup = BeautifulSoup(html)
    #get all the front page artical divs
    articles = soup.findAll('div', {'class':'blog-news featured_true'})
    articles+= soup.findAll('div', {'class':'blog-news featured_false'})
    urls = []
    for article in articles:
        #get the first hyper link in each article div
        link = article.find('a')
        url = "http://en.chessbase.com"+link['href']
        urls.append(url)
    return urls

def get_article_pgn_urls(article_url):
    #get the article html and put it through BeautifulSoup
    html = get_page_html(article_url)
    soup = BeautifulSoup(html)
    #get all of the hyper links
    links = soup.findAll('a')
    urls = []
    for link in links:
        #if the link has a href that ends with '.pgn'
        if link.has_key('href') and link['href'].endswith('.pgn'):
            url = "http://en.chessbase.com"+link['href']
            urls.append(url)
    return urls

if __name__=="__main__":

    #get the article urls
    article_urls = get_front_page_article_urls()

    #scrape each article
    pgn_urls = []
    for article_url in article_urls:
        print "Scraping..."
        pgn_urls+= get_article_pgn_urls(article_url)

    #print the results
    print "Done:"
    for pgn_url in pgn_urls:
        print pgn_url
