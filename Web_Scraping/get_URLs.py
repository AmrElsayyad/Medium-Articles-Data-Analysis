# importing necessary libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Defining needed variables
pause_time = 3      # time needed for page to load (in seconds)

# Getting the page
browser = webdriver.Firefox()
URL = 'https://datantify.com/lab/trendbar/'
page = browser.get(URL)
time.sleep(pause_time)
pause_time = 1

"""
Scrolling down until the page stops loading any more data
"""

body = browser.find_element_by_tag_name('body')
last_height = 0

# Check if the page stopped loading any more data
while last_height != browser.execute_script("return document.body.scrollHeight"):
    # Store the current height in last height
    last_height = browser.execute_script("return document.body.scrollHeight")
    # Scroll to the end of the page
    for i in range(5):
        body.send_keys(Keys.END)
    time.sleep(pause_time)
    # Load time increase
    pause_time += 0.1


def href(element):
    """
    A function that returns the href of an element
    """
    return element.get_attribute('href')


# Getting all the URLs in the page
URLs = pd.Series(browser.find_elements_by_xpath("//a[@class = 'text-dark']")).apply(href)

# Creating a dataframe and exporting to csv file
df = pd.DataFrame({'URL': URLs})
df.to_csv("Medium_URLs.csv", index=False)
