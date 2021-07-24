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

"""
Reading DataFrames
"""

URLs_df = pd.read_csv("Web_Scraping/Medium_URLs.csv")
data_df = pd.read_csv("Medium_Data.csv")
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
        browser.get(URLs_df['URL'][6958])
        time.sleep(wait_time)
        break
    except WebDriverException:
        browser.quit()

"""
Put your module here
"""


def text_to_num(txt):
    """
    :argument txt: text to be converted to number
    :return: number after conversion
    """
    multiplier = 1
    if txt == '':
        txt = '0'
    else:
        # Getting multiplier
        multipliers = {'K': pow(10, 3), 'M': pow(10, 6)}
        for multiplier in multipliers:
            if txt.__contains__(multiplier):
                txt = txt.replace(multiplier, '')
                multiplier = multipliers[multiplier]
                break
            else:
                multiplier = 1

    return float(txt) * multiplier


# Getting all the buttons
buttons = browser.find_elements_by_tag_name('button')

# Getting buttons that contain numbers
for i in range(len(buttons)):
    if any(char.isdigit() for char in buttons[i].text):
        """
        Note: The first button containing digits is the claps,
        and the next one is the responses.
        """
        # Getting claps
        claps_str = int(text_to_num(buttons[i].text))
        if claps_str == '':
            claps = 0
        else:
            claps = int(claps_str)

        # Getting responses
        responses_str = int(text_to_num(buttons[i + 1].text))
        if responses_str == '':
            responses = 0
        else:
            responses = int(responses_str)

        # Break the loop, no need to continue
        break

"""
Don't forget to quit the browser
"""

browser.quit()
