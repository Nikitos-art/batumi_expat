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
url = "https://www.myhome.ge/en/pr/15136995/Newly-finished-apartment-for-rent-Batumi-Sh.-Khimshiashvili-Street-1-rooms"
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
tree = etree.HTML(str(soup))

#################### Mongo client #####################################
client = MongoClient('127.0.0.1', 27017)
db = client['aptDB'] # Specify the database name
# cafes_rests = db.cafes_rests
apt_rests = db['apartments']  # Specify the collection name
#######################################################################


apt_list = tree.xpath('//div[@class="statement-row-search similar-prs"]//div[@class="statement-card"]')


for apt in apt_list:
    ### sizing needs cleaning
    size = apt.xpath('.//div[@class="item-size"]//text()')
    size_cleaned = [size[i] + '' + size[i+1] for i in range(0, len(size), 2)]
    ###links will be used later
    link = apt.xpath(".//a[@class='card-container']//@href")[0]
    ### price needs some mangling
    price = int(apt.xpath('.//b[@class="item-price-usd mr-2"]//text()')[0])

    apt_doc_obj = {
        'apt_price': f"${price}",
        'apt_size': size_cleaned[0],
        'apt_addr': apt.xpath('//div[@class="address"]//text()')[0],
        'ad_date': apt.xpath('.//div[@class="statement-date"]//text()')[0],
        'apt_link': link
    }

    driver.get(link)
    html_apt = driver.page_source
    soup_img = BeautifulSoup(html_apt, 'lxml')
    tree_apt = etree.HTML(str(soup_img))

    ### adding the image
    #apt_doc_obj['apt_img'] = tree_apt.xpath('.//img[@class="swiper-lazy h-100 swiper-lazy-loaded loaded"]//@src')[0]
    apt_doc_obj['apt_img'] = tree_apt.xpath(".//img[contains(@class, 'swiper-lazy')]/@src")[0]

    try:
        apt_rests.insert_one(apt_doc_obj)
        print('______' * 20)
        print('Inserted a document into DB.')
    except DuplicateKeyError:
        print(f"Apartment with link {apt_doc_obj['apt_link']} already exists.")


print('******' * 20)
print('Finished scraping')





