from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from lxml import etree
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


firefox_options = Options()
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options)
print('******' * 20)
print('Starting to scrape...')
url = "https://www.tripadvisor.com/Restaurants-g297576-c8-Batumi_Adjara_Region.html"
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
tree = etree.HTML(str(soup))

#################### Mongo client #####################################
client = MongoClient('127.0.0.1', 27017)
db = client['cafesDB'] # Specify the database name
# cafes_rests = db.cafes_rests
cafes_rests = db['cafes_rests_2']  # Specify the collection name
#######################################################################

cafes_l = tree.xpath('//div[@data-test-target="restaurants-list"]//ul')

cafes_list = []
for cafe in cafes_l:
    li_elements = cafe.findall('.//li')
    cafes_list.extend(li_elements)


for i in cafes_list:
    price = " "
    cuisine = " "
    tel = " "
    website = " "
    ### price tags require extra handling
    try:
        price_2 = i.xpath('.//span[@class="tqpbe"]//text()')[2]
    except IndexError:
        price = price
    else:
        price = price_2
    ### menu tag also require extra handling
    try:
        cuisine_2 = i.xpath('.//span[@class="tqpbe"]//text()')[1]
    except IndexError:
        cuisine = cuisine
    else:
        cuisine = cuisine_2

    cafe_link = 'https://www.tripadvisor.com' + i.xpath('.//a/@href')[0]

    doc_cafe_obj = {
        'cafe_name': i.xpath('.//h3//text()')[-1].strip(),
        'cafe_link': cafe_link,
        'cuisine': cuisine,
        'price': price,
        'reviews_count': i.xpath('.//span[@class="SUszq"]//text()')[0],
        'feedback': i.xpath('.//div[@class="EGgBc Ci"]//text()')[0]
    }

    driver.get(cafe_link)
    html_img = driver.page_source
    soup_img = BeautifulSoup(html_img, 'lxml')
    tree_img = etree.HTML(str(soup_img))

    ### website tag also require extra handling
    try:
        website_2 = tree_img.xpath('.//a[@class="YnKZo Ci Wc _S C AYHFM"]/@href')[0]
    except IndexError:
        website = website
    else:
        website = website_2

    ### tel tag also require extra handling
    try:
        tel_2 = tree_img.xpath('//span[@class="AYHFM"]//a[@class="BMQDV _F G- wSSLS SwZTJ"]/text()')[0]
    except IndexError:
        tel = tel
    else:
        tel = tel_2

    image_list = tree_img.xpath('//img[@class="basicImg"]/@src')
    for ima in image_list:
        if 'media-cdn.tripadvisor.com' in ima:
            doc_cafe_obj['cafe_img'] = ima
            break

    doc_cafe_obj['cafe_tel'] = tel

    ### address and rating handler
    add_rat_handler = tree_img.xpath('//a[@class="AYHFM"]//text()')

    doc_cafe_obj['address'] = add_rat_handler[2:][0]
    doc_cafe_obj['rating'] = ",".join(add_rat_handler[:2]).replace(',', '')

    ### open time handler
    work_time_handler = tree_img.xpath('//span[@class="mMkhr"]//text()')[2:]
    work_time_handler = list(filter(lambda item: item != '\xa0', work_time_handler))
    work_time_handler = ",".join(work_time_handler).replace(',', '')

    doc_cafe_obj['work_time'] = work_time_handler
    doc_cafe_obj['cafe_website'] = website

    try:
        cafes_rests.insert_one(doc_cafe_obj)
        print('______' * 20)
        print('Inserted a document into DB.')
    except DuplicateKeyError:
        print(f"Cafe with name {doc_cafe_obj['cafe_name']} already exists.")

print('******' * 20)
print('Scraping finished.')




