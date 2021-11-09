import subprocess
import sys
import os
from typing import Text
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    import selenium
except:
    install("selenium")
try:
    import pandas
except:
    install("pandas")
try:
    import tqdm
except:
    install("tqdm")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from tqdm import tqdm
import datetime

chrome_options = Options()
#chrome_options.set_headless()
#chrome_options.add_argument('start-maximized')

print('\n\n-------------------------------- Starting Scrape -------------------------------\n\n')
driver = webdriver.Chrome(options=chrome_options)
if len(sys.argv)>1:
    driver.get(sys.argv[1])
else:
    driver.get("https://www.boliga.dk/resultat?propertyType=3&zipCodes=1000-2990")

driver.implicitly_wait(5)

homes = []
df = None
data = {'url': [],
        'post_nummer': [],
        'boligtype': [],
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
        'salgsmaned': [],
        'salgsar': [],

    }
dt = datetime.datetime.today()

old_df = None
try:
    if os.path.isfile('boliga_data_being_sold_best.csv'):
        old_df = pd.read_csv('boliga_data_being_sold_best.csv')
except:
    pass

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
    for site in driver.find_elements_by_tag_name('a.house-list-item'):
        try:
            url = site.get_attribute('href')
            urls = old_df[old_df['url'].str.contains(url)]
            if old_df is not None and len(urls) > 0:
                try:
                    data["url"].append(urls["url"].iloc[0])
                except:
                    data["url"].append("")
                try:
                    data["post_nummer"].append(urls["post_nummer"].iloc[0])
                except:
                    data["post_nummer"].append("")
                try:
                    data["boligtype"].append(urls["boligtype"].iloc[0])
                except:
                    data["boligtype"].append("")
                try:
                    data["boligstorrelse"].append(urls["boligstorrelse"].iloc[0])
                except:
                    data["boligstorrelse"].append("")
                try:
                    data["grundstorrelse"].append(urls["grundstorrelse"].iloc[0])
                except:
                    data["grundstorrelse"].append("")
                try:
                    data["vaerelser"].append(urls["vaerelser"].iloc[0])
                except:
                    data["vaerelser"].append("")
                try:
                    data["etage"].append(urls["etage"].iloc[0])
                except:
                    data["etage"].append("")
                try:
                    data["byggeår"].append(urls["byggeår"].iloc[0])
                except:
                    data["byggeår"].append("")
                try:
                    data["om_byggeår"].append(urls["om_byggeår"].iloc[0])
                except:
                    data["om_byggeår"].append("")
                try:
                    data["skatter"].append(urls["skatter"].iloc[0])
                except:
                    data["skatter"].append("")
                try:
                    data["boligareal_tinglyst"].append(urls["boligareal_tinglyst"].iloc[0])
                except:
                    data["boligareal_tinglyst"].append("")
                try:
                    data["toiletter"].append(urls["toiletter"].iloc[0])
                except:
                    data["toiletter"].append("")
                try:
                    data["badevaerelser"].append(urls["badevaerelser"].iloc[0])
                except:
                    data["badevaerelser"].append("")
                try:
                    data["pris"].append(urls["pris"].iloc[0])
                except:
                    data["pris"].append("")
                try:
                    data["handelstype"].append(urls["handelstype"].iloc[0])
                except:
                    data["handelstype"].append("")
                try:
                    data["salgsmaned"].append(urls["salgsmaned"].iloc[0])
                except:
                    data["salgsmaned"].append("")
                try:
                    data["salgsar"].append(urls["salgsar"].iloc[0])
                except:
                    data["salgsar"].append("")
            else:
                homes.append(Home(url))
        except:
            pass
    next_page()

def next_page():
    try:
        driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-housing-list/div[2]/app-housing-list-results/div/div[1]/div[3]/div/div/div[3]/app-pagination/div/div[4]/a').click()
        time.sleep(5)
    except:
        last_page = True

for i in tqdm(range(int(driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-housing-list/div[2]/app-housing-list-results/div/div[1]/div[3]/div/div/div[3]/app-pagination/div/div[4]/div/a').text))):
    take_all()
    break

for home in tqdm(homes):
    if(home.url == 'https://www.boliga.dk/resultat' or home.url == None):continue
    time.sleep(1)
    driver.get(str(home.url))
    time.sleep(1)
    try:
        home.price = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bvs/div/div[4]/div/div/div[1]/div[1]/div/app-bvs-property-price/div/div[2]/span[1]').text
        driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bvs/div/div[4]/div/div/div[1]/div[1]/div/app-bvs-property-price/div/div[1]/a').click()
    except:
        continue

    #Post_nummer
    try:
        data['url'].append(home.url)
        ele = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[1]/div/app-bbr-inner-details/div/div[1]/div[1]/div[1]/div[1]/span')
        ele = ele.text.split('\n')
        ele = str(ele[0]+" "+ele[1])
        ele = ele.replace('"',"")
        data["post_nummer"].append(ele)
    except:
        data["post_nummer"].append(' ')

    #boligtype
    try:
        ele = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[1]/div/app-bbr-inner-details/div/div[1]/div[1]/div[1]/div[1]/app-property-label/label/span')
        data["boligtype"].append(ele.text)
    except:
        data["boligtype"].append(' ')

    #Boligstorrelse
    try:
        ele = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[1]/div/app-bbr-inner-details/div/div[1]/div[1]/div[2]/div/app-property-detail-list/ul/li[1]/app-property-detail/app-tooltip/div/span[3]')
        ele = ele.text.split('(BBR): ')[1].split(' m')
        data["boligstorrelse"].append(ele[0])
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
        ele = ele.text.split(': ')
        ele = ele[1].split(' kr')
        data["skatter"].append(ele[0])
    except:
        data["skatter"].append(' ')

    #Etage
    try:
        ele = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[1]/div/app-bbr-inner-details/div/div[1]/div[1]/div[2]/div/app-property-detail-list/ul/li[4]/app-property-detail/app-tooltip/div/span[3]')
        ele = ele.text.split(": ")
        ele = ele[1].replace(".","")
        data["etage"].append(ele)
    except:
        data["etage"].append(' ')

    #Boligareal_tinglyst
    try:
        ele = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[1]/div/app-bbr-inner-details/div/div[1]/div[1]/div[2]/div/app-property-detail-list/ul/li[8]/app-property-detail/app-tooltip/div/span[3]')
        ele = ele.text.split(': ')[1].split(' m')
        data["boligareal_tinglyst"].append(ele[0])
    except:
        data["boligareal_tinglyst"].append(' ')

    #Detaljerede boliginformationer
    try:
        driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[3]/app-bbr-details-tabs/app-property-information/div/div[1]/ul/li[1]/div[1]/span').click()
    except:
        print('failed')
    time.sleep(1)
    
    #Toiletter
    try:
        data["toiletter"].append(driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[3]/app-bbr-details-tabs/app-property-information/div/div[2]/div/div/app-generic-property-info-content[1]/div/div[2]/div/div[6]/div/span').text)
    except:
        data["toiletter"].append(' ')

    #Badevaerelser
    try:
        data["badevaerelser"].append(driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[3]/app-bbr-details-tabs/app-property-information/div/div[2]/div/div/app-generic-property-info-content[1]/div/div[2]/div/div[8]/div/span').text)
    except:
        data["badevaerelser"].append(' ')

    #pris
    try:
        ele = home.price
        ele = ele.split('\n')
        if len(ele)==2:
            ele = ele[1]
            ele = ele.split(' kr')[0]
            ele = ele.replace(".","")
            data["pris"].append(ele)
        else:
            ele = ele[0]
            ele = ele.split(' kr')[0]
            ele = ele.replace(".","")
            data["pris"].append(ele)
    except:
        data["pris"].append(' ')

    #Bygning
    try:
        driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[3]/app-bbr-details-tabs/app-property-information/div/div[1]/ul/li[7]').click()
    except:
        print('failed')
    time.sleep(1)
    
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
        ele = driver.find_element_by_xpath('/html/body/app-root/app-scroll-position-restoration/app-main-layout/app-bbr-inner/div[3]/app-bbr-details-tabs/app-property-information/div/div[2]/div/div/app-generic-property-info-content[2]/div/div[2]/div/div[7]/div/span')
        data["om_byggeår"].append(ele.text)
    except:
        data["om_byggeår"].append(' ')
    
    try:
        data["salgsmaned"] = dt.month
        data["salgsar"] = dt.year
    except:
        pass
    
    df = pd.DataFrame(data,columns=['url','post_nummer','boligtype','boligstorrelse','grundstorrelse','vaerelser','etage','byggeår','om_byggeår','skatter','boligareal_tinglyst','toiletter','badevaerelser','pris','salgsmaned','salgsar'])
    if len(sys.argv)>2:
        df.to_csv(sys.argv[2])
    else:
        df.to_csv('boliga_data_being_sold_scrabed.csv',index=False)