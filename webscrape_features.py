from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup as soup
import re
import math
import pandas as pd

#reading restaurant id and happycow page

rest_data	= pd.read_csv("restaurants_test.csv", encoding = "ISO-8859-1")
rest_id 	= rest_data.Data_ID
rest_url	= rest_data.Happycow_page 

#reading list of proxies

prox_data	= pd.read_csv("proxy.csv", encoding = "ISO-8859-1")
prox_ip		= prox_data.Proxy
prox_port	= prox_data.Port

#reading list of user agents

ua_data		= pd.read_csv("user_agent.csv", encoding = "ISO-8859-1")
ua_id		= ua_data.User_agent

ffp = webdriver.FirefoxProfile()

#creating a firefox driver

headers = "Data ID, Full Address, Street Address, Locality, Postal Code, Website, Facebook , Number of photos, Features\n"
data = list()
data.append(headers)
switch_count = 0

# setting load preferences - setting user agent id, proxy type, proxy ip and port number 
 
ffp.set_preference("network.proxy.type", 1)
ffp.set_preference("network.proxy.http", prox_ip[0])
ffp.set_preference("network.proxy.http_port", prox_ip[0])
ffp.set_preference("general.useragent.override", ua_id[0])
driver = webdriver.Firefox(firefox_profile = ffp)

prox_count = 0
ua_count = 0

for i in range(len(rest_id)):
	
	if (i%20 == 0):

		prox_count	= prox_count+1
		ua_count	= ua_count+1
		driver.close()
		
		print ("switching IP to")
		print (prox_ip[prox_count%len(prox_ip)])
		print ("switching Useragent to")
		print (ua_id[ua_count%len(ua_id)])
		
		ffp = webdriver.FirefoxProfile()
		ffp.set_preference("network.proxy.type", 1)
		ffp.set_preference("network.proxy.http", prox_ip[prox_count%len(prox_ip)])
		ffp.set_preference("network.proxy.http_port", prox_ip[prox_count%len(prox_ip)])
		ffp.set_preference("general.useragent.override", ua_id[ua_count%len(ua_id)])
		driver = webdriver.Firefox(firefox_profile = ffp)
		
	my_url 	= str(rest_url[i])
	driver.get(my_url)
	
	page_html  	= driver.page_source
	soup_page  	= soup(page_html,'html.parser')
	data_id 	= str(rest_id[i])
	
	addrcontain	= soup_page.findAll(itemprop = "streetAddress")
	if (addrcontain != []):
		addr_full	= addrcontain[0].text.strip()
		addr_split	= re.split(',', addr_full)
		addr_street	= addr_split[0]
	else:
		addr_full	= []
		addr_split	= []
		addr_street	= []

	if (len (addr_split) == 2):
		addr_area = addr_split[1]
	else:
		addr_area = ""

	postcontain	= soup_page.findAll(itemprop = "postalCode")

	if (postcontain != []):
		postal_code	= soup_page.findAll(itemprop = "postalCode")[0].text.strip()
	else:
		postal_code = ""

	webcontain	= soup_page.findAll(attrs = {"class":"url"})
	if (webcontain != []):
		website_	= re.search('href="(.*?)"', str(webcontain)).group(1)
	else: 
		website_ = ""

	fbcontain	= soup_page.findAll("a", class_="facebook--blue--def--color")
	if (fbcontain != []):
		facebook_	= re.search('href="(.*?)"', str(fbcontain)).group(1)
	else:
		facebook_ = ""
	
	photocontain= soup_page.findAll(title = "View all photos of this venue")
	if (photocontain != []):
		num_photos	= re.findall('View all (.*?) photos', photocontain[0].text)[0]
	else:
		num_photos	= '0'

	feat_		= str()	
	featcontain	= soup_page.findAll("div", class_="box__map__body")

	if (featcontain != []):
		pattern		= re.compile('\<li title="(.*?)"\>\<i')
		features	= pattern.findall(str(featcontain[0].ul.li.ul))
		for j in range(len(features)):
			feat_ = features[j]+","+feat_

	data.append(data_id+","
		+addr_full+","
		+addr_street+","
		+addr_area+","
		+postal_code+","
		+website_+","
		+facebook_+","
		+num_photos+ ","
		+feat_
		+"\n") 

filename="D:/Data_science/Webscrape/restaurants_features.csv"
with open(filename,"w", encoding="utf-8") as f:
	f.writelines(data)
driver.quit()