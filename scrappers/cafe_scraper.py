from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import lxml

# Configure Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--headless")
# Create a new Selenium webdriver instance with the configured options
driver = webdriver.Chrome(options=chrome_options)

url = "https://www.tripadvisor.com/Restaurants-g297576-c8-Batumi_Adjara_Region.html"
# Use Selenium to open the webpage
driver.get(url)
# Get the page source after the JavaScript has rendered
html = driver.page_source
# Create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(html, 'lxml')

cafes_list = soup.find("div", {"data-test-target": "restaurants-list"})
li_elements = cafes_list.find_all('li')


#################### Mongo client #####################################
client = MongoClient('127.0.0.1', 27017)

db = client['cafesDB']
cafes_rests = db.cafes_rests
#######################################################################
for i in li_elements:
    price = " "
    menu = " "
    ### price tags require extra handling
    try:
        price_2 = i.find("div", {"class": "hBcUX XFrjQ mIBqD"}).find_all("span", {"class": "tqpbe"})[1].text
    except IndexError:
        price = price
    else:
        price = price_2
    ### menu tag also require extra handling
    try:
        menu_2 = i.find("div", {"class": "hBcUX XFrjQ mIBqD"}).find("span", {"class": "d"}).text
    except AttributeError:
        menu = menu
    else:
        menu = menu_2

    doc_cafe_obj = {
        'cafe_name': i.find("h3").text.split('. ')[1],
        'num_of_rev': i.find("span", {"class": "SUszq"}).text,
        'open_time': i.find_all("span", {"class": "tqpbe"})[1].text,
        'food': i.find("div", {"class": "hBcUX XFrjQ mIBqD"}).find_all("span", {"class": "tqpbe"})[0].text,
        'price': price,
        'menu': menu,
        'feedback': i.find("div", {"class": "EGgBc Ci"}).text
    }

    try:
        cafes_rests.insert_one(doc_cafe_obj)
    except DuplicateKeyError:
        print(f"Cafe with name {doc_cafe_obj['cafe_name']} already exists.")


###################### Scrape To JSON #############################
# json_cafe_list = []
# with open('cafes.json', 'w', encoding='utf-8') as w_file:
# json.dump(json_cafe_list, w_file, indent=4, ensure_ascii=False)
# json_cafe_list.append(json_cafe_obj)




