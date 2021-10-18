import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

#install('selenium')
#install('BeautifulSoup4')
install('requests')

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests

URL = "https://realpython.github.io/fake-jobs/"

driver = webdriver.Chrome()
driver.get("https://www.boligportal.dk/lejligheder/")

#Click away terms of use
driver.implicitly_wait(8)
driver.find_element_by_id("declineButton").click()

driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div/div/div[2]/div[7]/div[1]/div[1]/div/a/div/div[1]").click()
driver.back()