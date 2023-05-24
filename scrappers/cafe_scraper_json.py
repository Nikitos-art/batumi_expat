from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import json

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

url = "https://www.tripadvisor.com/Restaurants-g297576-c8-Batumi_Adjara_Region.html"
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
tree = etree.HTML(str(soup))


cafes_l = tree.xpath('//div[@data-test-target="restaurants-list"]//ul')

cafes_list = []
for cafe in cafes_l:
    li_elements = cafe.findall('.//li')
    cafes_list.extend(li_elements)


json_cafe_list = []

for i in cafes_list:
    price = " "
    cuisine = " "
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

    json_cafe_obj = {
        'cafe_name': i.xpath('.//h3//text()')[-1].strip(),
        'cafe_link': cafe_link,
        'cuisine': cuisine,
        'price': price,
        'reviews_count': i.xpath('.//span[@class="SUszq"]//text()')[0],
        'feedback': i.xpath('.//div[@class="EGgBc Ci"]//text()')
    }

    driver.get(cafe_link)
    html_img = driver.page_source
    soup_img = BeautifulSoup(html_img, 'lxml')
    tree_img = etree.HTML(str(soup_img))

    image_list = tree_img.xpath('//img[@class="basicImg"]/@src')
    for ima in image_list:
        if 'media-cdn.tripadvisor.com' in ima:
            json_cafe_obj['cafe_img'] = ima
            break

    json_cafe_obj['cafe_tel'] = tree_img.xpath('//span[@class="AYHFM"]//a[@class="BMQDV _F G- wSSLS SwZTJ"]/text()')

    ### address and rating handler
    add_rat_handler = tree_img.xpath('//a[@class="AYHFM"]//text()')

    json_cafe_obj['address'] = add_rat_handler[2:]
    json_cafe_obj['rating'] = ",".join(add_rat_handler[:2]).replace(',', '')

    ### open time handler
    work_time_handler = tree_img.xpath('//span[@class="mMkhr"]//text()')[2:]
    work_time_handler = list(filter(lambda item: item != '\xa0', work_time_handler))
    work_time_handler = ",".join(work_time_handler).replace(',', '')

    json_cafe_obj['work_time'] = work_time_handler
    json_cafe_obj['cafe_website'] = tree_img.xpath('.//a[@class="YnKZo Ci Wc _S C AYHFM"]/@href')

    json_cafe_list.append(json_cafe_obj)


with open('cafes.json', 'w', encoding='utf-8') as w_file:
    json.dump(json_cafe_list, w_file, indent=4, ensure_ascii=False)
