from re import match
import subprocess
import sys
from typing import Text

import selenium

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from tqdm import tqdm

chrome_options = Options()
#chrome_options.set_headless()
chrome_options.add_argument('start-maximized')

print('\n\n-------------------------------- Starting Scrape -------------------------------\n\n')
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.boliga.dk/salg/resultater?searchTab=1&propertyType=3&salesDateMin=2018&saleType=1&zipcodeFrom=1000&zipcodeTo=2990&sort=date-d&page=1")

driver.implicitly_wait(5)

homes = []
first_page = True
last_page = False

class Home:
    def __init__(self,url) -> None:
        self.url = url
    
    def rewritemonth(self,input):
        if(input == 'jan.'):
            return 1
        elif(input == 'feb.'):
            return 2
        elif(input == 'mar.'):
            return 3
        elif(input == 'apr.'):
            return 4
        elif(input == 'maj'):
            return 5
        elif(input == 'jun.'):
            return 6
        elif(input == 'jul.'):
            return 7
        elif(input == 'aug.'):
            return 8
        elif(input == 'sep.'):
            return 9
        elif(input == 'okt.'):
            return 10
        elif(input == 'nov.'):
            return 11
        elif(input == 'dec.'):
            return 12

#Click away terms of use
driver.find_element_by_id("declineButton").click()


def take_all():
    for site in driver.find_elements_by_tag_name('a.text-primary.font-weight-bolder.text-left'):
        try:
            homes.append(Home(site.get_attribute('href')))
        except:
            print(site.get_attribute('href'))
    next_page()
def next_page():
    try:
        driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-properties-list/div[3]/div/div/app-pagination/div/div[4]/a').click()
        time.sleep(5)
    except:
        last_page = True

for i in range(726):
    take_all()

data = {'url': [],
        'post_nummer': [],
        'boligstorrelse': [],
        'grundstorrelse': [],
        'vaerelser': [],
        'etage': [],
        'byggeår':[],
        'om_byggeår':[],
        'skatter': [],
        'boligareal_tinglyst': [],
        'toiletter': [],
        'badevaerelser': [],
        'pris': [],
        'handelstype': [],
        'salgsmaned': [],
        'salgsar': []
    }

for home in tqdm(homes):
    driver.get(home.url)
    home.price = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-inner/div[3]/app-sales-overview/div/div[1]/div/div/div[2]/table/tbody/tr[1]/td[2]/span[2]').text
    home.salgsdato = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-inner/div[3]/app-sales-overview/div/div[1]/div/div/div[2]/table/tbody/tr[1]/td[3]/span[2]').text
    home.handelstype = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-inner/div[3]/app-sales-overview/div/div[1]/div/div/div[2]/table/tbody/tr[1]/td[4]/span[2]').text
    driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-sold-inner/div[3]/div/a[1]').click()
    time.sleep(1)


    #Post_nummer
    try:
        data['url'].append(home.url)
        ele = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[1]/div/app-bbr-inner-details/div/div[1]/div[1]/div[1]/div[1]/span')
        ele = ele.text.split("\n")
        ele = ele[1].split(" ")
        data["post_nummer"].append(ele[0])
    except:
        data["post_nummer"].append(' ')
    #Boligstorrelse
    try:
        ele = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[1]/div/app-bbr-inner-details/div/div[1]/div[1]/div[2]/div/app-property-detail-list/ul/li[1]/app-property-detail/app-tooltip/div/span[3]')
        ele = [int(s) for s in ele.text.split() if s.isdigit()]
        ele = [""+str(s) for s in ele]
        temp = ""
        for n in ele: temp += n
        data["boligstorrelse"].append(temp)
    except:
        data["boligstorrelse"].append(' ')
    #Grundstorrelse
    try:
        ele = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[1]/div/app-bbr-inner-details/div/div[1]/div[1]/div[2]/div/app-property-detail-list/ul/li[2]/app-property-detail/app-tooltip/div/span[3]')
        ele = [int(s) for s in ele.text.split() if s.isdigit()]
        ele = [""+str(s) for s in ele]
        temp = ""
        for n in ele: temp += n
        data["grundstorrelse"].append(temp)
    except:
        data["grundstorrelse"].append(' ')
    #Vaerelser
    try:
        ele = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[1]/div/app-bbr-inner-details/div/div[1]/div[1]/div[2]/div/app-property-detail-list/ul/li[3]/app-property-detail/app-tooltip/div/span[3]')
        ele = [int(s) for s in ele.text.split() if s.isdigit()]
        ele = [""+str(s) for s in ele]
        temp = ""
        for n in ele: temp += n
        data["vaerelser"].append(temp)
    except:
        data["vaerelser"].append(' ')
    #Skatter
    try:
        ele = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[1]/div/app-bbr-inner-details/div/div[1]/div[1]/div[2]/div/app-property-detail-list/ul/li[6]/app-property-detail/app-tooltip/div/span[3]')
        ele = [int(s) for s in ele.text.split() if s.isdigit()]
        ele = [""+str(s) for s in ele]
        temp = ""
        for n in ele: temp += n
        data["skatter"].append(temp)
    except:
        data["skatter"].append(' ')
    #Etage
    try:
        ele = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[1]/div/app-bbr-inner-details/div/div[1]/div[1]/div[2]/div/app-property-detail-list/ul/li[4]/app-property-detail/app-tooltip/div/span[3]')
        ele = ele.text.split(" ")
        ele = ele[1].split(".")
        data["etage"].append(ele[0])
    except:
        data["etage"].append(' ')
    #Boligareal_tinglyst
    try:
        ele = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[1]/div/app-bbr-inner-details/div/div[1]/div[1]/div[2]/div/app-property-detail-list/ul/li[8]/app-property-detail/app-tooltip/div/span[3]')
        ele = [int(s) for s in ele.text.split() if s.isdigit()]
        ele = [""+str(s) for s in ele]
        temp = ""
        for n in ele: temp += n
        data["boligareal_tinglyst"].append(temp)
    except:
        data["boligareal_tinglyst"].append(' ')

    #Detaljerede boliginformationer
    try:
        driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[4]/app-bbr-details-tabs/app-property-information/div/div[1]/ul/li[1]/div[1]/span').click()
    except:
        print('failed')
    time.sleep(0.5)
    #Toiletter
    try:
        data["toiletter"].append(driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[4]/app-bbr-details-tabs/app-property-information/div/div[2]/div/div/app-generic-property-info-content[1]/div/div[2]/div/div[6]/div/span').text)
    except:
        data["toiletter"].append(' ')
    #Badevaerelser
    try:
        data["badevaerelser"].append(driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[4]/app-bbr-details-tabs/app-property-information/div/div[2]/div/div/app-generic-property-info-content[1]/div/div[2]/div/div[8]/div/span').text)
    except:
        data["badevaerelser"].append(' ')

    #Tidligere salg af boligen
    try:
        driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[4]/app-bbr-details-tabs/app-property-information/div/div[1]/ul/li[4]/div[1]/span').click()
    except:
        print('failed')
    time.sleep(0.5)
    #pris
    try:
        ele = str(home.price)
        ele = ele.split(".")
        temp = ""
        for n in ele: temp += n
        data["pris"].append(temp)
    except:
        data["pris"].append(' ')

    #handelstype
    try:
        data["handelstype"].append(home.handelstype)
    except:
        data["handelstype"].append(' ')

    #Bygning
    try:
        driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[4]/app-bbr-details-tabs/app-property-information/div/div[1]/ul/li[7]/div[1]/span').click()
    except:
        print('failed')
    time.sleep(0.5)
    
    #Byggeår
    try:
        ele = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[1]/div/app-bbr-inner-details/div/div[1]/div[1]/div[2]/div/app-property-detail-list/ul/li[5]/app-property-detail/app-tooltip/div/span[3]')
        ele = [int(s) for s in ele.text.split() if s.isdigit()]
        ele = [""+str(s) for s in ele]
        temp = ""
        for n in ele: temp += n
        data["byggeår"].append(temp)
    except:
        data["byggeår"].append(' ')
    
    #Om bygnings år
    try:
        ele = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[4]/app-bbr-details-tabs/app-property-information/div/div[2]/div/div/app-generic-property-info-content[2]/div/div[2]/div/div[7]/div/span')
        data["om_byggeår"].append(ele.text)
    except:
        data["om_byggeår"].append(' ')

    #salgsdato
    try:
        ele = home.salgsdato.split(' ')
        ele[1] = home.rewritemonth(ele[1])
        data["salgsmaned"].append(ele[1])
        data["salgsar"].append(ele[2])
    except:
        data["salgsmaned"].append(' ')
        data["salgsar"].append(' ')

    df = pd.DataFrame(data,columns=['url','post_nummer','boligstorrelse','grundstorrelse','vaerelser','etage','byggeår','om_byggeår','skatter','boligareal_tinglyst','toiletter','badevaerelser','pris','handelstype','salgsmaned','salgsar'])
    df.to_csv('boliga_test_data.csv',index=False)