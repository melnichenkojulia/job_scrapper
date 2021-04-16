import datetime
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import math
from JobScrapping.utils.database import update_vacancies



def get_urls_parsing(client, date):
    urls = []
    for doc in client["job_seeking"]["vacancy"].find():
        if 'time_parsed' not in doc.keys() or doc['time_parsed'] < date:
            urls.append(doc['_id'])
    return urls


def parse_vacancy_page_by_link(driver, url):
    driver.get(url)
    flag = driver.find_elements_by_css_selector(".f-main-wrapper")[0].text
    if 'Вакансия закрыта' in flag:
        return {'url': url, 'time_parsed': datetime.datetime.now()}
    f_text = driver.find_elements_by_tag_name("h1")[0].text
    city = driver.find_elements_by_css_selector("p.address-string > span")[0].text
    key_skills = driver.find_elements_by_css_selector("app-clusters li li")
    details = driver.find_elements_by_css_selector('#description-wrap')[0].text
    sk = []
    for skill in key_skills:
        sk.append(skill.text)
    return {
        'url': url,
        'title': f_text,
        'city': city,
        'skills': sk,
        'details': details,
        'time_parsed': datetime.datetime.now(),
    }

def parse_vacancies_pages(driver, urls):
    vac_collect = []
    for i_url in urls:
        info = parse_vacancy_page_by_link(driver, i_url)
        vac_collect.append(info)
        update_vacancies([info])

def parse_vacancy_main_page(page):
    title = page.find_elements_by_css_selector('.card-title > a')[0].text
    company = page.find_elements_by_css_selector('.company-profile-name')[0].text
    location = page.find_elements_by_css_selector('.location')[0].text
    salary= page.find_elements_by_css_selector('.salary')[0].text
    link=page.find_elements_by_css_selector('.card-title > a')[0].get_attribute('href')
    return {
        'title': title,
        'company': company,
        'location': location,
        'salary': salary or None,
        # 'link': link,
        'url': link,
        # 'time_parsed': datetime.now(),
    }


def connect():
    driver = webdriver.Chrome('resources/chromedriver')
    driver.get('http://www.rabota.ua/')
    time.sleep(3)
    return driver

def count_vacancies(vacancy_name):

    driver=connect()
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'input'))).send_keys(vacancy_name)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'input'))).send_keys(Keys.ENTER)
    driver.find_elements_by_class_name("card")
    vac_num = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#ctl00_content_vacancyList_ltCount > span')))
    page_num = int(vac_num.text) / 40
    page_num = math.ceil(page_num)
    return page_num,driver



def parse_title(vacancy_name):
    page_num,driver=count_vacancies(vacancy_name)
    page = 1
    vac_collect=[]

    while True:
        f_text = driver.find_elements_by_class_name("card")
        print(page)
        for f in f_text:
            vac_collect.append(parse_vacancy_main_page(f))

        if page == page_num:
            break
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#ctl00_content_vacancyList_gridList_ctl43_pagerInnerTable > dd.nextbtn'))).click()
        page = page + 1
    return vac_collect

