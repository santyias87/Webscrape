from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup as soup
from contextlib import closing

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                log_error('Could not fetch url: ' + url)
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None
        
def get_page_count(url):
    page_html = simple_get(url)
    soup_page = soup(page_html,'html.parser')
    results_count = int(soup_page.find("span", {"class":"total-results"}).text.strip())
    page_count = int(round(results_count/81))
    return page_count


CAT_TYPE_MAP = {
    "0": "Restaurant",
    "1": "Store",
    "2": "Store",
    "3": "Bakery",
    "4": "B&B",
    "5": "Delivery",
    "6": "Catering",
    "7": "Organization",
    "8": "Farmer's market",
    "10": "Food Truck",
    "14": "Professional",
    "13": "Juice Bar",
    "99": "Other",
}

def get_type(cat):
    return CAT_TYPE_MAP.get(cat, "MarketVendor")

def get_page_data(url):
    page_html =  simple_get(url)
    soup_page = soup(page_html,'html.parser')
    container = soup_page.findAll("div", {"class":"js-venues venues__item"})
    data = list()
    for	contain	in	container:
        data_id	=	contain["data-id"]
        boxinf	=	contain.div.div.a.div.div.div.div
        name_	=	boxinf.h4.text.strip()
        detinf	=	contain.div.div.a.div.div.find_next_sibling("div").div
        lat_	=	detinf["data-lat"]
        lon_	=	detinf["data-lng"]
        rating_	=	detinf["data-rating"]
        phone_	=	detinf["data-phone"]
        res_url	=	"https://happycow.net/"+detinf["data-url"]
        dat_cat =	detinf["data-category"]
        dat_vgn	=	detinf["data-vegan"]
        dat_veg	=	detinf["data-vegonly"]
        dat_ent	=	detinf["data-entrytype"]
        if (dat_vgn == '1' and dat_veg == '1'):
            ven_opt = "Vegan"
        elif(dat_vgn == '0' and dat_veg == '1'):
            ven_opt = "Vegetarian"
        else:
            ven_opt = "Veg Options"

        ven_typ = get_type(dat_cat)

        one_data = [data_id, name_, ven_typ, ven_opt, rating_, lat_, lon_, res_url]
        one_data_str = ",".join(one_data)
        data.append(one_data_str)
    return data

def fetch_city_happy_data(filename, url):
    all_data = list()
    for count in range(1, get_page_count(url) + 1):
        page_url = url + "&page=" + str(count)
        all_data += get_page_data(page_url)
    with open(filename, "w") as f:
        f.write("\n".join(all_data).encode('utf-8'))

CITY_URL_MAP = {
    "BERLIN": ("berlin.csv", "https://www.happycow.net/searchmap?location=&radius=15&metric=mi&limit=81&order=default&lat=52.5062&lng=13.3296")
}

def main():
    for city in CITY_URL_MAP:
        filename, url = CITY_URL_MAP[city]
        fetch_city_happy_data(filename, url)

if __name__ == '__main__':
    main()