from difflib import SequenceMatcher
from hashlib import sha512
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import os
import time
import logging
from pyvirtualdisplay import Display

#logging.basicConfig(filename='scrape.log',level=logging.DEBUG)

class ScrapeDriver:
    def __init__(self, url, driver='firefox', headless=True):
        self.driver_type = driver
        self.url = url
        if headless:
            self.display = Display(visible=0, size=(800, 600))
            self.display.start()

        if driver == 'chrome':
            self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                          chrome_options=chrome_options
                         )
        elif driver == 'firefox':
            self.driver = webdriver.Firefox()
        
        return
    
    def get(self, url):
        self.driver.get(url)

    @staticmethod
    def similar(a, b):
        #https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
        return SequenceMatcher(None, a, b).ratio()

    def save_screenshot_by_element(self, filename, element_name='body'):
        #https://stackoverflow.com/questions/41721734/taking-screenshot-of-full-page-with-selenium-python-chromedriver
        element = self.driver.find_element_by_tag_name(element_name)

        if self.driver_type == 'chrome':
            element_png = element.screenshot(str(filename) + '.png')
        elif self.driver_type =='firefox':
            element_png = element.screenshot_as_png
            with open("{}.png".format(filename), "wb") as file:
                file.write(element_png)
        return

    def compute_hash_element(self, element_name='body'):
        #https://stackoverflow.com/questions/15732752/good-way-to-compare-huge-strings-in-python
        element = self.driver.find_element_by_tag_name(element_name)
        html_source = element.get_attribute('innerHTML')
        return sha512(html_source.encode('utf-8')).digest()

    def get_full_page_source(self):
        self.html_source = self.driver.page_source
        return self.html_source

    def search_html(self, terms):
        try:
            html_source = self.html_source
        except:
            html_source = self.get_full_page_source()
        finally:
            for term in terms:
                if term in html_source:
                    return True
                else:
                    return False

    def _quit(self):
        self.driver.quit()
        self.display.stop()
        return