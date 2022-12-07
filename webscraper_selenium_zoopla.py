from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import yaml
import collections

# Sale Price: Our response variable
# Number of bedrooms
# Square footage
# Description
# Address

#class Config:
    

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
        XPATH_FOR_REGULAR_PROP_PAGE_LIST = self.get_config()['xpath_for_regular_prop_page_list']
        # XPATH_FOR_FEATURED_PROP_PAGE_LIST = self.get_config()['xpath_for_featured_prop_page_list']
        
        time.sleep(2)
        regular_prop_container = self.driver.find_element(by=By.XPATH, value=XPATH_FOR_REGULAR_PROP_PAGE_LIST) # Change this xpath with the xpath the current page has in their properties
        regular_prop_list = regular_prop_container.find_elements(by=By.XPATH, value='./div')
        print(regular_prop_list)
        # featured_prop_container = self.driver.find_element(by=By.XPATH, value=XPATH_FOR_FEATURED_PROP_PAGE_LIST) # Change this xpath with the xpath the current page has in their properties
        # featured_prop_list = featured_prop_container.find_elements(by=By.XPATH, value='./div')

        # prop_list = regular_prop_list + featured_prop_list

        for prop in regular_prop_list:
            reg_a_tag = prop.find_element(by=By.TAG_NAME, value='a')
            reg_link = reg_a_tag.get_attribute('href')
            self.prop_url_list.append(reg_link)

        # for prop in featured_prop_list:
        #     feat_a_tag = featured_prop_container.find_element(by=By.TAG_NAME, value='a')
        #     feat_link = feat_a_tag.get_attribute('href')
        #     self.prop_url_list.append(feat_link)
        
        print(self.prop_url_list)
        print(len(self.prop_url_list))

        return self.prop_url_list

    def extract_prop_data(self):
        print(self.prop_url_list)
        for num, url in enumerate(self.prop_url_list, start=1):
            self.driver.get(url)
            time.sleep(2) # Wait a couple of seconds, so the website doesn't suspect you are a bot
            XPATH_SUMMARY = self.get_config()['xpath_summary']
            XPATH_PRICE = self.get_config()['xpath_price']
            XPATH_ADDRESS = self.get_config()['xpath_address']
            XPATH_NUM_BEDROOMS = self.get_config()['xpath_num_bedrooms']
           # XPATH_NUM_BATHROOMS = self.get_config()['xpath_num_bathrooms']

            summary = self.driver.find_element(by=By.XPATH, value=XPATH_SUMMARY)
            price = self.driver.find_element(by=By.XPATH, value=XPATH_PRICE)
            address = self.driver.find_element(by=By.XPATH, value=XPATH_ADDRESS)
            #num_bedrooms = self.driver.find_element(by=By.XPATH, value=XPATH_NUM_BEDROOMS)
            #num_bathrooms = self.driver.find_element(by=By.XPATH, value=XPATH_NUM_BATHROOMS)
            
            self.prop_dict[num]['summary'] = summary.text
            self.prop_dict[num]['price'] = price.text
            self.prop_dict[num]['address'] = address.text
            #self.prop_dict[num]['num_bedrooms'] = num_bedrooms.text 
            self.prop_dict[num]['link'] = url
            #self.prop_dict[num]['num_bathrooms'] = num_bathrooms.text
            #self.prop_dict[num]['num_receptions'] = num_receptions.text
        
        print(self.prop_dict)
    
    def get_csv(self):
        #TODO: read property data into a csv and save out
        pass

    def get_json(self):
        #TODO: read property data into a json and save out
        pass

if __name__ == "__main__":
    s = Scraper('config.yaml')
    s.get_config()
    s.handle_cookies()
    s.get_urls()
    s.extract_prop_data()

# TODO:
# sort out issue with the xpaths to get the list of links for specific property listings
# get list of links
# for each link in list, do scraping to find:
# price
# address label
# general tagline
# num bedrooms
# num bathrooms

