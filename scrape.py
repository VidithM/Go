import sys, requests, re
import _pickle as pickle

from bs4 import BeautifulSoup as BS
from manifest import Manifest
from requests.exceptions import Timeout

MAX_DEPTH = 2
MAX_PUSH = 10


q = []
num = 1

crawled = []
crawled_url = []

def scrape():
    global num
    while(len(q) > 0):
        url = q[0][0]
        depth = q[0][1]
        q.pop(0)
        keywords = []
        title = ''
        soup = None
        num += 1
        if(num%100 == 0):
            print(num)
        try:
            page_content = requests.get(url, timeout=10).content 
            soup = BS(page_content, 'html.parser')
            title = soup.title.text
        except Exception as e:
            if(e == KeyboardInterrupt):
                break
            continue
        
        for wrd in re.findall(r"[\w']+", title):
                keywords.append(wrd.lower())
        '''
        for elem in soup.find_all('h1'):
            for wrd in re.findall(r"[\w']+", elem.text):
                keywords.append(wrd.lower())
        '''
    
        index(keywords, url, title)
        if(depth == MAX_DEPTH):
            continue
        curr = 0
        for elem in soup.find_all('a'):
            if(curr == MAX_PUSH):
                break
            url = elem.get('href')
            if(validURL(url)):
                curr += 1
                crawled_url.append(url)
                q.append((url, depth + 1))

def validURL(url):
   try:
       return (url.index('http') == 0 and (not url in crawled_url))
   except:
       return False

def index(keywords, url, title):
    add = Manifest(keywords, url, title)
    crawled.append(add)

initial = open('initial.txt', 'r')
for ln in initial:
    if('~' in ln):
        continue 
    else:
        q.append((ln.split('\n')[0], 0))

scrape()
out_file = open('index.byte', 'wb')
pickle.dump(crawled, out_file)
out_file.close()
