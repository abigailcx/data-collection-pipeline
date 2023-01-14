# **Data Collection Pipeline**

## Introduction
This property data webscraper, built with Python and Selenium, scrapes data from the Zoopla property website. It saves the the data in jpg, csv and json format, which can be used for property data analysis.

## Contents
This repo contains:
  - **zoopla_webscraper.py**: a webscraper to scrape zoopla.co.uk for data on property location, price, number of bedrooms, bathrooms and living rooms, as well as the url for the specific property page on Zoopla. Optionally, images can also be scraped


  - **config.yaml**: the configuration file containing information on:
    - which url to scrape
    - how many properties to get data for
    - names of json and csv output files
    - all necessary xpaths


  - **test_zoopla_webscraper.py**: unit tests for the webscraper

## Set up the Environment
Use the following command to ensure all the dependencies are installed.

`pip install -r requirements.txt`

## Run the Code
Navigate to the data-collection-pipeline repo after cloning it.
Use

`python3 zoopla_webscraper.py`

to run the zoopla webscraper.
The data scraped will be saved in the property_data file that will be automatically created in the data-collection-pipeline repo. Data can be saved as a csv file and as a json file. Image data is saved in a separate folder within the same location.

## The Configuration File
`config.yaml` is where the following should be defined:
- **url**: the url of the page to be scraped
- **page_size**: the number of properties for which to scrape data
- **extract_image_data**: a boolean value to tell the program whether or not to scrape image data. Use `!!bool true` to scrape image data too. Otherwise, use `!!bool false`
- **json_outfile**: specifies the name of the json file for the data
- **csv_outfile**: specifies the name of the csv file for the data

The xpaths do not need to be changed.

Before running the scraper, ensure that all the options within `config.yaml` are correctly set. The default configurations scrape the 15 most recent properties in London without extracting image data. The output files are called `zoopla_data.json` and `zoopla_data.csv`.

## Output Files
Output files will be prepended with the date and time of creation. Multiple sequential runs of the webscraper can be made without previous data being overwritten.
