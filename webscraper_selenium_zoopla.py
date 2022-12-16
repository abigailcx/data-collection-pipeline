from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import collections
import os
import time
import yaml
import json
import pandas as pd
import urllib

class Scraper:
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.driver = webdriver.Chrome()
        self.prop_url_list = [] # empty list to add urls for each individual property page (zoopla)
        self.prop_dict = collections.defaultdict(dict)

    def get_config(self):
        with open(self.config_file, 'r') as f:
            config_dict = yaml.load(f, Loader=yaml.FullLoader)
        
        return config_dict

    def handle_cookies(self):
        URL = f"{self.get_config()['url']}&page_size={self.get_config()['page_size']}"
        self.driver.get(URL)
        time.sleep(2) # Wait a couple of seconds, so the website doesn't suspect you are a bot
        
        try:
            self.driver.switch_to_frame('gdpr-consent-notice') # This is the id of the frame
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@id="save"]')
            accept_cookies_button.click()

        except AttributeError: # If you have the latest version of Selenium, the code above won't run because the "switch_to_frame" is deprecated
            self.driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@id="save"]')
            accept_cookies_button.click()

        except:
            pass # If there is no cookies button, we won't find it, so we can pass


    def get_urls(self):
        # XPATH_FOR_REGULAR_PROP_PAGE_LIST = self.get_config()['xpath_for_regular_prop_page_list']
        # XPATH_FOR_FEATURED_PROP_PAGE_LIST = self.get_config()['xpath_for_featured_prop_page_list']
        xpath_regular_listings = '//div[@data-testid="regular-listings"]'
        regular_listings = self.driver.find_element(by=By.XPATH, value=xpath_regular_listings)
        regular_listings_class_attribute = regular_listings.get_attribute('class')
        self.driver
        time.sleep(2)
        regular_prop_container = self.driver.find_element(by=By.XPATH, value=f'//div[@class="{regular_listings_class_attribute}"]') # Change this xpath with the xpath the current page has in their properties
        regular_prop_list = regular_prop_container.find_elements(by=By.XPATH, value='./div')

        for prop in regular_prop_list:
            reg_a_tag = prop.find_element(by=By.TAG_NAME, value='a')
            reg_link = reg_a_tag.get_attribute('href')
            self.prop_url_list.append(reg_link)

        return self.prop_url_list


    def extract_prop_data(self):

        for num, url in enumerate(self.prop_url_list, start=1):
            self.driver.get(url)
            time.sleep(2) # Wait a couple of seconds, so the website doesn't suspect you are a bot
            
            XPATH_SUMMARY = self.get_config()['xpath_summary']
            XPATH_PRICE = self.get_config()['xpath_price']
            XPATH_ADDRESS = self.get_config()['xpath_address']
            XPATH_ROOM_COUNT = self.get_config()['xpath_room_count']
            XPATH_NUM_ROOMS = self.get_config()['xpath_num_rooms']
            XPATH_IMAGE_GALLERY = self.get_config()['xpath_image_gallery']
            XPATH_IMAGES = self.get_config()['xpath_images']

            summary = self.driver.find_element(by=By.XPATH, value=XPATH_SUMMARY)
            price = self.driver.find_element(by=By.XPATH, value=XPATH_PRICE)
            address = self.driver.find_element(by=By.XPATH, value=XPATH_ADDRESS)
            room_count = self.driver.find_elements(by=By.XPATH, value=XPATH_ROOM_COUNT)
            image_gallery_elements = self.driver.find_elements(by=By.XPATH, value=XPATH_IMAGE_GALLERY)

            room_info = []
            for elem in room_count:
                room_info.append(elem.find_element(by=By.XPATH, value=XPATH_NUM_ROOMS).text)
          
            self.prop_dict[num]['summary'] = summary.text
            self.prop_dict[num]['price'] = price.text
            self.prop_dict[num]['address'] = address.text
            self.prop_dict[num]['num_rooms'] = room_info
            self.prop_dict[num]['link'] = url
            
            img_src = []
            for img in image_gallery_elements:
                print(img)
                img_src.append(img.find_element(by=By.XPATH, value=XPATH_IMAGES).get_attribute('src'))
                
                try:
                    next_image_button = self.driver.find_element(by=By.XPATH, value='//button[@data-testid="arrow_right"]')
                    next_image_button.click()
                    time.sleep(2)
                except:
                    print("There is no next button on this page.")
                    pass

            #breakpoint()
            for idx, url in enumerate(img_src, start=1):
                filedir_img = f"./image_data/{datetime.now().strftime('%d-%m-%Y')}/{num}_{address.text}/{idx}.jpg"
                os.makedirs(os.path.dirname(filedir_img), exist_ok=True)
                urllib.request.urlretrieve(url, filedir_img)
        
        print(self.prop_dict)


    def get_csv(self):
        filedir_csv = f"./csv_data/{datetime.now().strftime('%d-%m-%Y_%H%M%S')}_{self.get_config()['csv_outfile']}"
        os.makedirs(os.path.dirname(filedir_csv), exist_ok=True)
        df = pd.DataFrame(self.prop_dict)
        df = df.transpose()
        df.to_csv(filedir_csv)


    def get_json(self):
        prop_data = json.dumps(self.prop_dict, sort_keys=False, indent=4, ensure_ascii=False)
        filedir_json = f"./json_data/{datetime.now().strftime('%d-%m-%Y_%H%M%S')}_{self.get_config()['json_outfile']}"
        os.makedirs(os.path.dirname(filedir_json), exist_ok=True)
        with open(filedir_json, 'w') as outfile:
            outfile.write(prop_data)


    def scrape(self):
        self.get_config()
        self.handle_cookies()
        self.get_urls()
        self.extract_prop_data()


if __name__ == "__main__":
    s = Scraper('config.yaml')
    s.scrape()
    s.get_json()
    s.get_csv()
