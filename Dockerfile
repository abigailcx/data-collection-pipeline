# choose base image
FROM python:latest

# define working directory
WORKDIR /Users/agc/AiCore/data-collection-pipeline



# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Add Google Chrome
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Update apt:
RUN apt-get -y update

# Install google chrome:
RUN apt-get install -y google-chrome-stable

# Download chromedriver
# Download zipfile containing latest chromedriver release
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

# unzip
RUN apt-get install -yqq unzip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/



# put scraper contents in the container
COPY . .

# install dependencies
RUN pip install -r requirements.txt


# run main file
ENTRYPOINT ["python3", "webscraper_selenium_zoopla.py"]