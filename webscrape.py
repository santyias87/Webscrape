from urllib.request import urlopen 
from bs4 import BeautifulSoup as bSoup
from urllib.request import Request as req

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,de;q=0.7',
            'Connection': 'keep-alive'}

temp_url = 'https://www.happycow.net/searchmap?location=Berlin,%20Germany&radius=15&metric=mi&limit=81&order=default&lat=52.5062&lng=13.3296'
my_url = req (url = temp_url, headers = headers)
#uClient = urlopen(my_url)
#page_html = uClient.read()
#uClient.close()
#print (page_html)
#page_soup = bSoup(page_html, "html.parser")

from urllib import robotparser

re = robotparser.RobotFileParser()
re.set_url(my_url)
re.read()
print(re.can_fetch('*',my_url))