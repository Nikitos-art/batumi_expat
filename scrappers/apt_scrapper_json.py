from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import json

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
print('******' * 20)
print('Starting to scrape...')
url = "https://www.myhome.ge/en/pr/15136995/Newly-finished-apartment-for-rent-Batumi-Sh.-Khimshiashvili-Street-1-rooms"
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
tree = etree.HTML(str(soup))


apt_list = tree.xpath('//div[@class="statement-row-search similar-prs"]//div[@class="statement-card"]')

### first get all the links
# links = []
# for apt in apt_list:
#     links.append(apt.xpath("//a[@class='card-container']//@href"))

###

json_apt_list = []

for apt in apt_list:
    ### sizing needs cleaning
    size = apt.xpath('.//div[@class="item-size"]//text()')
    size_cleaned = [size[i] + '' + size[i+1] for i in range(0, len(size), 2)]
    ###links will be used later
    link = apt.xpath(".//a[@class='card-container']//@href")[0]
    json_apt_obj = {
        'apt_price': apt.xpath('.//b[@class="item-price-usd mr-2"]//text()'),
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
    json_apt_obj['apt_img'] = tree_apt.xpath('.//img[@class="swiper-lazy h-100 swiper-lazy-loaded loaded"]//@src')[0]
    print('added an item into json')
    json_apt_list.append(json_apt_obj)

with open('apts.json', 'w', encoding='utf-8') as w_file:
    json.dump(json_apt_list, w_file, indent=4, ensure_ascii=False)

print('******' * 20)
print('Finished scraping')



