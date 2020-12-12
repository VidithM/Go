import sys, requests
from bs4 import BeautifulSoup as BS

#Queue for scraping BFS
q = []

def scrape():
    while(len(q) > 0):
        url = q[0]
        q.pop()
        keywords = []

        page_content = requests.get(url).content 
        soup = BS(page_content, 'html.parser')
        for elem in soup.find_all('h1'):
            keywords.append(elem.text)
        for elem in soup.find_all('h2'):
            keywords.append(elem.text)
        
        for elem in soup.find_all('a'):
            print(elem.get('href'))

def validURL(url):
    return (url.index('http') == 0) 

def index():
    pass


q.append("https://www.msnbc.com/")
scrape()