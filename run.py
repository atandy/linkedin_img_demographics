import time
import random
import bs4
from sqlalchemy import create_engine
from scrape_page import ScrapeDriver
import pandas as pd
import os
import logging

logging.basicConfig(
    filename='scrape_linkedin.log', 
    filemode='w', 
    format='%(asctime)s:%(levelname)s:%(message)s', 
    level=logging.DEBUG)

env = 'Testing'

def linkedin_login():
    '''Open browser and log in using your LinkedIn credentials'''
    url = 'http://www.linkedin.com'
    username = os.getenv('LINKEDIN_USERNAME')
    password = os.getenv('LINKEDIN_PASSWORD')

    sd = ScrapeDriver(url)
    sd.get(url)
    sd.driver.find_element_by_class_name('login-email').send_keys(username)
    time.sleep(1)
    sd.driver.find_element_by_class_name('login-password').send_keys(password)
    time.sleep(1)
    sd.driver.find_element_by_class_name('submit-button').submit()
    time.sleep(1)
    return sd

def go_reco(pagenum, sd):
    logging.info("Now working on page: {}".format(pagenum))
    sd.driver.execute_script('window.scrollTo(0, {})'.format(random.randint(500,700)))
    #sd.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(random.randint(1,3))
    next_button = sd.driver.find_element_by_class_name('next')
    next_button.location_once_scrolled_into_view

    # need to scroll to bottom of page before getting profiles.
    soup = bs4.BeautifulSoup(sd.driver.page_source, "html.parser")
    profiles = soup.find_all('div', {'class':'presence-entity__image'})
    
    for p in profiles:
        name = p.attrs['aria-label']
        try:
            image = p.attrs['style'].split('background-image: url(')[1].rstrip(');')
        except:
            image = None
        d = { "name": name, "image": image }
        df = pd.DataFrame.from_dict(d, orient='index').transpose()
        logging.info("Inserting to database: {}".format(df))
        if env != 'Testing':
            df.to_sql('linkedin_people', engine, if_exists='append')
    
    next_button.click()
    pagenum += 1
    time.sleep(random.randint(1,2))
    
    go_reco(pagenum, sd)

if __name__ == '__main__':
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    sd = linkedin_login()
    search_string = 'https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%221441%22%5D&facetGeoRegion=%5B%22us%3A84%22%5D&keywords=Senior%20Software%20Engineer&origin=FACETED_SEARCH'
    sd.get(search_string)
    time.sleep(1)
    go_reco(1, sd)