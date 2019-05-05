from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
import re
import math

#reading latitudes and longitudes 

import pandas as pd

city_data	= pd.read_csv("geo.csv", encoding = "ISO-8859-1")
city_names  = city_data.city
city_lat 	= city_data.lat
city_lng	= city_data.lng
#city_con	= city_data.country	
	
# setting load preferences - disabling flash, image and CSS loading

ffp = webdriver.FirefoxProfile()
ffp.set_preference('permissions.default.stylesheet', 2)
ffp.set_preference('permissions.default.image', 2)
ffp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

#creating a firefox driver

driver = webdriver.Firefox(firefox_profile = ffp)

feature = {'Juice Bar':21,'Macrobiotic':12,
	 'Organic':13, 'Raw food':14, 'Salad Bar':20, 'Take Out':24, 'American':5, 'Asian':28, 'Australian':47, 'Brazilian':46, 'British':30, 'Caribbean':31,
	 'Chinese':7, 'European':34, 'French':35, 'Fusion':36, 'German':37,'Indian':8, 'International':9, 'Italian':10,'Japanese':11, 'Latin':45, 
	 'Mediterranean':18, 'Mexican':25, 'Middle Eastern':39, 'Spanish':40, 'Taiwanese':41, 'Thai':15, 'Vietnamese':42, 'Western':16}

#feature = { 'Bakery':29, 'Pizza':6, 'Beer-Wine':22, 'Buffet':17, 'Catering':32, 'Delivery':23, 'Fast food':19, 'Gluten-free':43, 'Juice Bar':21,'Macrobiotic':12,
#	 'Organic':13, 'Raw food':14, 'Salad Bar':20, 'Take Out':24, 'American':5, 'Asian':28, 'Australian':47, 'Brazilian':46, 'British':30, 'Caribbean':31,
#	 'Chinese':7, 'European':34, 'French':35, 'Fusion':36, 'German':37,'Indian':8, 'International':9, 'Italian':10,'Japanese':11, 'Latin':45, 
#	 'Mediterranean':18, 'Mexican':25, 'Middle Eastern':39, 'Spanish':40, 'Taiwanese':41, 'Thai':15, 'Vietnamese':42, 'Western':16}

Cat = ['Juice Bar','Macrobiotic',
	 'Organic', 'Raw food', 'Salad Bar', 'Take Out', 'American', 'Asian', 'Australian', 'Brazilian', 'British', 'Caribbean',
	 'Chinese', 'European', 'French', 'Fusion', 'German','Indian', 'International', 'Italian','Japanese', 'Latin', 
	 'Mediterranean', 'Mexican', 'Middle Eastern', 'Spanish', 'Taiwanese', 'Thai', 'Vietnamese', 'Western']

#Cat = ['Bakery', 'Pizza', 'Beer-Wine', 'Buffet', 'Catering', 'Delivery', 'Fast food', 'Gluten-free', 'Juice Bar','Macrobiotic',
#	 'Organic', 'Raw food', 'Salad Bar', 'Take Out', 'American', 'Asian', 'Australian', 'Brazilian', 'British', 'Caribbean',
#	 'Chinese', 'European', 'French', 'Fusion', 'German','Indian', 'International', 'Italian','Japanese', 'Latin', 
#	 'Mediterranean', 'Mexican', 'Middle Eastern', 'Spanish', 'Taiwanese', 'Thai', 'Vietnamese', 'Western']

#headers="Data ID, Phone \n"

#data.append(headers)

	
for j in range(len(Cat)):
	data= list();

	for i in range(len(city_names)):

		my_url = "https://www.happycow.net/searchmap?=&filters=vegan-vegetarian&ft="+str(feature[Cat[j]])+"&radius=25&metric=mi&limit=81&order=default&lat="+str(city_lat[i])+"&lng="+str(city_lng[i])
		driver.get(my_url)
		page_html = driver.page_source
		soup_page = soup(page_html,'html.parser')

		results_count = int(soup_page.find("span", {"class":"total-results"}).text.strip())
		loop_count = math.ceil(results_count/81)

		for count in range(1, (loop_count+1)):

			if (count != 1):
				my_url = "https://www.happycow.net/searchmap?=&filters=vegan-vegetarian&ft="+str(feature[Cat[j]])+"&radius=25&metric=mi&limit=81&order=default&lat="+str(city_lat[i])+"&lng="+str(city_lng[i])+"&page="+str(count)
				driver.get(my_url)
				page_html=driver.page_source
				soup_page = soup(page_html,'html.parser')

			for details in soup_page.findAll(attrs = {"class":"js-venues venues__item"}):
				data.append(details["data-id"]+"\n")
	filename="category_"+Cat[j]+".csv"			
	with open(filename,"w", encoding="utf-8") as f:
		f.writelines(data)
driver.quit()	



