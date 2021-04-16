import sys
from selenium import webdriver
import datetime
import pymongo
from utils import utils

if __name__ == '__main__':
    client = pymongo.MongoClient()
    urls = utils.get_urls_parsing(client,datetime.datetime.now()-datetime.timedelta(days=5))
    if len(urls)!=0:
        driver = webdriver.Chrome('resources/chromedriver')
    else:
        sys.exit()
    utils.parse_vacancies_pages(driver, urls)
    driver.close()
