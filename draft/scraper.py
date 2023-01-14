import json
import requests
from bs4 import BeautifulSoup

# This could include code to scroll the website, click a next button on product details page or simply navigate to the next required webpage.

# Just think about what tasks you usually perform while browsing different websites.

prop_dict = {}
url = "https://www.zoopla.co.uk/for-sale/property/london/the-ridgeway-e4/e4-6pu/?q=E4+6PU&results_sort=newest_listings&search_source=refine&radius=1&view_type=list"

properties = []
page_idx = 1

while page_idx < 6:
    print(f"{url}&pn={page_idx}")
    response = requests.get(f"{url}&pn={page_idx}")
    html = response.content
    html2 = BeautifulSoup(html, 'html.parser')
    properties_page = html2.find_all('div', attrs={"class": "c-PJLV c-PJLV-ieIaIjy-css"})
    properties.extend(properties_page)
    page_idx += 1
#print(properties)

    # price = prop.find("p", attrs={"data-testid": "listing-price"})
    # num_bathrooms = prop.find("span", attrs={"class": "c-PJLV"})
    # title = prop.find("h2", attrs={"data-testid": "listing-title"})
    # address = prop.find("h3", attrs={"class": "c-eFZDwI"})
    # date_listed = prop.find("li", attrs={"class": "c-eUGvCx"})

for num, prop in enumerate(properties, start=1):
    #print(prop.prettify())
    prop_dict[num] = {}
    price = prop.find("p", attrs={"data-testid": "listing-price"})
    title = prop.find("h2", attrs={"data-testid": "listing-title"})
    address = prop.find("h3", attrs={"class": "c-eFZDwI"})
    date_listed = prop.find("li", attrs={"class": "c-eUGvCx"})
    prop_dict[num]["title"] = title.text
    prop_dict[num]["price"] = price.text
    prop_dict[num]["address"] = address.text
    prop_dict[num]["date_listed"] = date_listed.text
    page_idx += 1

prop_data = json.dumps(prop_dict, sort_keys=False, indent=4, ensure_ascii=False)
with open('property_data.json', 'w') as outfile:
    outfile.write(prop_data)