"""
Needed libraries and variables
"""

# Importing necessary libraries
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import nltk
import random
import time

# Defining needed variables
wait_time = 1               # Time for page to load
browser = webdriver         # Initializing webdriver
URL = str()                 # Article URL
title = str()               # Title text
head_image = str()          # Header image link
images_num = int()          # Number of images in the article
h1_num = int()              # h1 headers count
h2_num = int()              # h2 headers count
p_num = int()               # Paragraphs count
p_word_count_avg = int()    # Word count average per paragraph
quotes_num = int()          # Number of quotes per article
publication = str()         # Publication name
writer = str()              # Writer name
claps = int()               # Number of claps
responses = int()           # Number of responses
page_counter = 0            # Counter to count how many page has been scraped
page_counter_limit = 10     # How many pages to be written each time

# Reading the data csv file
URLs_df = pd.read_csv("Web_Scraping/Medium_URLs.csv")

# Get the proxies list
proxies = pd.read_csv("Web_Scraping/proxies.csv")["Proxy"]

# Initializing counter
counter = random.randrange(0, len(proxies))

"""
Starting browser
"""

options = Options()
options.headless = True
options.add_argument("--disable-extensions")
for i in range(0, len(proxies)):
    try:
        browser = webdriver.Firefox(options=options, proxy=proxies[counter % len(proxies)])
        counter += 1
        """
        Choose URL here
        """
        browser.get(URLs_df['URL'][0])
        time.sleep(wait_time)
        break
    except WebDriverException:
        browser.quit()

"""
Put your module here
"""

# Getting Publication

try:
    publication = browser.find_element_by_xpath(
        "//*[@id='root']/div/div[3]/div[5]/div/div[2]/div[1]/div/div/div[1]/div[3]/span/span/div/div/h2/a"
    ).text
except NoSuchElementException:
    publication = ''

# Getting date and read time

if publication == '':
    # If there's no publication
    paragraphs = browser.find_elements_by_tag_name('p')
    for p in paragraphs:
        if p.text.__contains__(" min read"):
            date_and_time = p.text.split("·")
            date = date_and_time[0]
            read_time = int(date_and_time[1].replace(" min read", ""))

else:
    # If there's a publication

    divs = browser.find_elements_by_tag_name('div')

    for div in divs:
        if div.text.__contains__(" min read"):
            div_text = div.text.split("\n")
            for txt in div_text:
                if txt.__contains__(" min read"):
                    date_and_time = txt.split(" · ")
                    date = date_and_time[0]
                    read_time = int(date_and_time[1].replace(" min read", ""))
                    break
            break

"""
Don't forget to quit the browser
"""

browser.quit()
