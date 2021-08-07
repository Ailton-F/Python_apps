import pandas
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep


opt = Options()
opt.add_argument('window-size=400,800')
#opt.add_argument('--headless')

nav = webdriver.Chrome(executable_path=r"chromedriver.exe", options=opt)
nav.get('https://www.airbnb.com')

sleep(5)

input_place = nav.find_element_by_tag_name('input')
input_place.send_keys('são paulo')
input_place.submit()

sleep(1)

button_stay = nav.find_element_by_css_selector('button > img')
button_stay.click()

sleep(1)

nextButton = nav.find_elements_by_tag_name('button')[-1]
nextButton.click()

sleep(1)

adultButton = nav.find_elements_by_css_selector('button > span > svg > path[d="m2 16h28m-14-14v28"]')[0]
adultButton.click()
sleep(1)
adultButton.click()

sleep(1)

searchButton = nav.find_elements_by_tag_name('button')[-1]
searchButton.click()

sleep(1)

nav.refresh()

sleep(3)

okButtonCookies = nav.find_elements_by_tag_name('button')[1]
okButtonCookies.click()

sleep(4)

fontcode = nav.page_source

site = BeautifulSoup(fontcode, 'html.parser')

hotels_data = []

hotels = site.findAll('div', attrs={'itemprop': 'itemListElement'})

for hotel in hotels:
    hotel_desc = hotel.find('meta', attrs={'itemprop': 'name'})
    hotel_url = hotel.find('meta', attrs={'itemprop': 'url'})
    hotel_desc_content = hotel_desc['content']
    hotel_url_content = hotel_url['content']

    print('Descrição:', hotel_desc_content)
    print('URL:', hotel_url_content)

    hotel_details = hotel.find('div', attrs={'style': 'margin-bottom: 2px;'})
    hotel_details_list = hotel_details.findAll('li')
    hotel_details_list = "".join([details.text for details in hotel_details])
    print('Detalhes da hospedagem: ', hotel_details_list)

    price = hotel.findAll('span')[-1].text
    print('Preço da hospedagem: ', price)

    print()

    hotels_data.append([hotel_desc_content, hotel_url_content, hotel_details_list, price])

print(pandas.DataFrame(hotels_data, columns=['Descrição', 'Link', 'Detalhes', 'Preço']))
