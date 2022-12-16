import json
import pandas
import requests
from bs4 import BeautifulSoup
import config


class House:
    
    def __init__(self):
        self.title = title
        self.price = price
        self.address = address
        self.date_listed = date_listed

class Scraper:
    
    def __init__(self, url):
        self.url = url
        self.page_idx = 1
        self.properties = []
        self.prop_dict = {}


    def parse_site(self):
        response = requests.get(f"{self.url}&pn={self.page_idx}")
        html = response.content
        parsed = BeautifulSoup(html, 'html.parser')
        
        return parsed

    def scrape_zoopla(self):
        while self.page_idx < 6:
            print(f"{self.url}&pn={self.page_idx}")
            
            properties_page = self.parse_site().find_all('div', attrs={"class": "c-PJLV c-PJLV-ieIaIjy-css"})
            self.properties.extend(properties_page)
            self.page_idx += 1

        for num, prop in enumerate(self.properties, start=1):
            self.prop_dict[num] = {}
            price = prop.find("p", attrs={"data-testid": "listing-price"})
            title = prop.find("h2", attrs={"data-testid": "listing-title"})
            address = prop.find("h3", attrs={"class": "c-eFZDwI"})
            date_listed = prop.find("li", attrs={"class": "c-eUGvCx"})
            self.prop_dict[num]["title"] = title.text
            self.prop_dict[num]["price"] = price.text
            self.prop_dict[num]["address"] = address.text
            self.prop_dict[num]["date_listed"] = date_listed.text
        
        return self.prop_dict

def scrape():
    s = Scraper(config.url)
    s.parse_site()
    s.scrape_zoopla()

scrape()
