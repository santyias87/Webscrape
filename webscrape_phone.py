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

headers="Data ID, Phone \n"
data = list()
data.append(headers)
	

for i in range(len(city_names)):

	my_url = "https://www.happycow.net/searchmap?location=&radius=15&metric=mi&limit=81&order=default&lat="+str(city_lat[i])+"&lng="+str(city_lng[i])
	driver.get(my_url)

	page_html = driver.page_source

	#f = open("check.html", "w")
	#f.write(page_html)
	#f.close()

	soup_page = soup(page_html,'html.parser')
	results_count = int(soup_page.find("span", {"class":"total-results"}).text.strip())
	loop_count = math.ceil(results_count/81)

	for count in range(1, (loop_count+1)):

		if (count != 1):

			my_url="https://www.happycow.net/searchmap?location=&radius=15&metric=mi&limit=81&order=default&lat="+str(city_lat[i])+"&lng="+str(city_lng[i])+"&page="+str(count)
			driver.get(my_url)
			page_html=driver.page_source
			soup_page = soup(page_html,'html.parser')
		
		container = soup_page.findAll("div", {"class":"js-venues venues__item"})

		for	contain	in	container:
			data_id	=	contain["data-id"]
			boxinf	=	contain.div.div.a.div.div.div.div
			name_	=	boxinf.h4.text.strip()
			
			#address	=	boxinf.p.find_next("p").text.strip()
			#addr	=	re.split(",",address)
			#city_	=	city_names[i]
			#country_=	city_con[i]
			#loc_cod	=	addr[len(addr)-1].strip()
			#street_	=	addr[0]

			#print ("processing #",i+1,": ",name_)
			
			#if(len(addr)==5):
			#	loc_=street_+" "+addr[1]
			#else:
			#	loc_=street_

			detinf	=	contain.div.div.a.div.div.find_next_sibling("div").div
			#moreinf =   detinf.div.find_next_sibling("div").div
			#lat_	=	detinf["data-lat"]
			#lon_	=	detinf["data-lng"]
			#rating_	=	detinf["data-rating"]
			phone_	=	str(detinf["data-phone"])
			#res_url	=	"https://happycow.net/"+detinf["data-url"]
			#dat_cat =	detinf["data-category"]
			#dat_vgn	=	detinf["data-vegan"]
			#dat_veg	=	detinf["data-vegonly"]
			#dat_ent	=	detinf["data-entrytype"]
			#num_rev =   moreinf.span.text.replace("(","").replace(")","")
			#price   =   len(moreinf.ul.find_next("ul").li.find_next("li").findAll('i',{'class':'fa fa-dollar price--fill'}))


			#if (dat_vgn == '1' and dat_veg == '1'):
			#	ven_opt = "Vegan"
			#elif(dat_vgn == '0' and dat_veg == '1'):
			#	ven_opt = "Vegetarian"
			#else:
			#	ven_opt = "Veg Options"

			#if(dat_cat == '0'):
			#	ven_typ	= "Restaurant"
			#elif(dat_cat ==	'1' or dat_cat == '2'):
			#	ven_typ	= "Store"
			#elif(dat_cat ==	'7'):
			#	ven_typ	= "Organization"
			#elif(dat_cat ==	'14'):
			#	ven_typ	= "Professional"
			#elif(dat_cat ==	'13'):
			#	ven_typ	= "Juice Bar"
			#elif(dat_cat ==	'6'):
			#	ven_typ	= "Catering"
			#elif(dat_cat ==	'10'):
			#	ven_typ	= "Food Truck"
			#elif(dat_cat ==	'3'):
			#	ven_typ	= "Bakery"
			#elif(dat_cat ==	'5'):
			#	ven_typ	= "Delivery"
			#elif(dat_cat ==	'99'):
			#	ven_typ	= "Other"
			#elif(dat_cat ==	'8'):
			#	ven_typ	= "Farmer's market"
			#elif(dat_cat ==	'4'):
			#	ven_typ	= "B&B"
			#else:
			#	ven_typ	= "MarketVendor"

			#if (price == 1):
			#	price_ = "Cheap"
			#elif (price == 2):
			#	price_ = "Average"
			#else:
			#	price_ = "Expensive"

			data.append(data_id+","
				#+name_+","
				#+city_+","
				#+country_+","
				#+ven_typ+","
				#+ven_opt+","
				#+rating_+","
				#+num_rev+","
				#+price_+","
				#+lat_+","
				#+lon_+","
				+phone_+","
				#+res_url+
				"\n")
filename="restaurants_phone.csv"
with open(filename,"w", encoding="utf-8") as f:
	f.writelines(data)
driver.quit()