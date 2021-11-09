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
try:
    import requests
except:
    install("requests")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import json
from tqdm import tqdm
import requests

being_sold = pd.read_csv("boliga_data_being_sold_best.csv")
data_sold = pd.read_csv("boliga_data_sold_best.csv")

latitude = []
longitude = []
'''
for i in tqdm(range(len(being_sold))):
    address = being_sold["post_nummer"][i]
    request = json.loads(requests.get("https://api.opencagedata.com/geocode/v1/json?q="+address+"%2Cdanmark&key=03c48dae07364cabb7f121d8c1519492&no_annotations=1&language=en").text)
    latitude.append(request['results'][0]['geometry']['lat'])
    longitude.append(request['results'][0]['geometry']['lng'])
being_sold.insert(loc=2, column='latitude', value=latitude)
being_sold.insert(loc=3, column='longitude', value=longitude)
being_sold.to_csv("boliga_data_being_sold_best_updated.csv",index=False)
'''
latitude.clear()
longitude.clear()

for i in tqdm(range(len(data_sold))):
    address = data_sold["post_nummer"][i]
    try:
        request = json.loads(requests.get("https://api.opencagedata.com/geocode/v1/json?q="+address+"%2Cdanmark&key=03c48dae07364cabb7f121d8c1519492&no_annotations=1&language=en").text)
        latitude.append(request['results'][0]['geometry']['lat'])
        longitude.append(request['results'][0]['geometry']['lng'])
    except:
        latitude.append(" ")
        longitude.append(" ")
data_sold.insert(loc=2, column='latitude', value=latitude)
data_sold.insert(loc=3, column='longitude', value=longitude)
data_sold.to_csv("boliga_data_sold_best_updated.csv",index=False)