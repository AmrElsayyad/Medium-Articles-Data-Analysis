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
from urllib3.exceptions import MaxRetryError

# Downloading punctuation package for nltk
nltk.download('punkt')

# Defining needed variables
last_row = 0                # Last row in the URLs DataFrame that was collected
browser = webdriver         # Initializing webdriver
wait_time = 1               # Time for page to load
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
date = str()                # Date of the article
read_time = int()           # Estimated read time of the article in minutes
claps = int()               # Number of claps
responses = int()           # Number of responses
page_counter = 0            # Counter to count how many page has been scraped
page_counter_limit = 10     # How many pages to be written each time

# Defining needed functions


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


# Reading the URLs csv file
URLs_df = pd.read_csv("Medium_URLs.csv")

# Read DataFrame if it exists
try:
    data_df = pd.read_csv("../Medium_Data.csv")
    title_with_dash = '-'.join(data_df['Title'].iloc[-1].split(' '))
    last_row = URLs_df[URLs_df['URL'].apply(lambda txt: txt.__contains__(title_with_dash))].index[0] + 1
except FileNotFoundError:
    # Create a new one if it doesn't
    data_df = pd.DataFrame(
        columns=['URL', 'Title', 'Image', 'Images_num', 'h1_num', 'h2_num', 'Paragraphs_num',
                 'Paragraphs_Word_Count_avg', 'Quotes_num', 'Publication', 'Writer',
                 'Date', 'Read_Time', 'Claps', 'Responses'])

# Get the proxies list
proxies = pd.read_csv("proxies.csv")["Proxy"]

# Initializing counter
counter = random.randrange(0, len(proxies))

# Get Pages' content, continuing from last row
for URL in URLs_df['URL'][last_row:]:
    # Assuming failure until page data collection is complete
    failed = True
    # Keep trying until page data collection is successful
    while failed:
        try:
            # Setting up Firefox
            options = Options()
            options.headless = True
            options.add_argument("--disable-extensions")
            for i in range(0, len(proxies)):
                try:
                    browser = webdriver.Firefox(options=options, proxy=proxies[counter % len(proxies)])
                    counter += 1
                    browser.get(URL)
                    time.sleep(wait_time)
                    break
                except WebDriverException:
                    browser.quit()

            """
            Getting publication and writer
            """

            # Getting Publication

            try:
                publication = browser.find_element_by_xpath(
                    "//*[@id='root']/div/div[3]/div[5]/div/div[2]/div[1]/div/div/div[1]/div[3]/span/span/div/div/h2/a"
                ).text
            except NoSuchElementException:
                publication = ''

            # Getting Writer

            if publication == '':
                # If there's no publication, use this xpath to find the writer
                try:
                    writer = browser.find_element_by_xpath(
                        "//*[@id='root']/div/div[3]/div[5]/div/div[2]/div[2]/div/div/div/div[1]/h2/a"
                    ).text.replace("More from ", "")
                except NoSuchElementException:
                    # If this element is not found, then probably the page is not found
                    # Quit the browser and skip this page
                    browser.quit()
                    failed = False
                    break
            else:
                # If there's a publication, use this xpath to find the writer
                writer = browser.find_element_by_xpath(
                    "//*[@id='root']/div/div[3]/div[5]/div/div[2]/div[1]/div/div/div[1]/div[1]/"
                    "span/span/div[2]/div/h2/a"
                ).text

            """
            Getting images
            """

            # Getting number of images
            figures = browser.find_elements_by_xpath("//figure[contains(@class, paragraph-image)]")
            images_num = len(figures)

            # Getting the header image
            head_image = ''
            if len(figures) > 0:
                try:
                    img = figures[0].find_element_by_tag_name('img')
                    # Check if the image is a valid header image by checking the size
                    if int(img.get_attribute('width')) > 650:
                        head_image = img.get_attribute('src')
                except NoSuchElementException:
                    head_image = ''

            """
            Getting the title

            1- Split the URL, and get the last piece
            2- Split that and leave the code at the end
            3- Join all the words together with space in between
            """

            title = " ".join(browser.current_url.split('/')[-1].split('-')[:-1])

            """
            Getting the headers
            """

            try:
                # Getting number of h1 elements
                h1_num = len(browser.find_elements_by_tag_name('h1'))
            except NoSuchElementException:
                h1_num = 0

            # Getting h2 elements
            h2s = browser.find_elements_by_tag_name('h2')

            # Filter h2 elements
            for i in range(len(h2s)):
                if h2s[i].text != '':
                    h2s = h2s[i + 1:]
                    break

            # Getting number of h2 elements
            h2_num = 0
            for h2 in h2s:
                if h2.text == '':
                    # The last h2 element is followed by an empty one
                    break
                else:
                    h2_num += 1

            """
            Getting paragraphs
            """

            # Getting all paragraph elements
            paragraphs = browser.find_elements_by_tag_name('p')

            # Filter paragraphs
            for i in range(len(paragraphs)):
                if paragraphs[i].text == 'Top highlight':
                    paragraphs = paragraphs[i + 1:]
                    break
            # If 'Top highlights' wasn't found then start with the nearest not empty paragraph
            for i in range(len(paragraphs)):
                if paragraphs[i].text == '':
                    continue
                else:
                    paragraphs = paragraphs[i:]
                    break

            # Initializing Number of Paragraphs with 0
            p_num = 0

            # Getting average paragraphs' word count
            p_word_count_list = list()
            for p in paragraphs:
                if p.text == '':
                    # The last paragraph is followed by an empty one
                    break
                else:
                    p_num += 1
                    p_word_count_list.append(len(nltk.word_tokenize(p.text)))
            p_word_count_avg = int(np.round(np.mean(p_word_count_list)))

            """
            Getting number of quotes
            """

            try:
                quotes_num = len(browser.find_elements_by_tag_name('blockquote'))
            except NoSuchElementException:
                quotes_num = 0

            """
            Getting date and read time
            """

            if publication == '':
                # If there's no publication

                for p in paragraphs:
                    if p.text.__contains__(", 20") and p.text.__contains__(" min read"):
                        date_and_time = p.text.split("·")
                        date = date_and_time[0]
                        read_time = int(date_and_time[1].replace(" min read", ""))

            else:
                # If there's a publication

                divs = browser.find_elements_by_tag_name('div')

                for div in divs:
                    if div.text.__contains__(" min read"):
                        div_text = div.text.split("\n")
                        for text in div_text:
                            if text.__contains__(" min read"):
                                date_and_time = text.split(" · ")
                                date = date_and_time[0]
                                read_time = int(date_and_time[1].replace(" min read", ""))
                                break
                        break

            """
            Getting claps and responses
            """

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
            Appending to DataFrame and quitting the browser
            """

            # Appending to DataFrame
            data_df.loc[len(data_df.index)] = \
                [browser.current_url, title, head_image, images_num, h1_num, h2_num, p_num, p_word_count_avg,
                 quotes_num, publication, writer, date, read_time, claps, responses]

            # Quitting the browser
            browser.quit()

            # Increase page counter and if limit is reached write to csv
            page_counter += 1
            if page_counter == page_counter_limit:
                page_counter = 0  # Reset counter
                if data_df.shape[0] > 0:
                    data_df.to_csv("../Medium_Data.csv", index=False)

            """
            Success
            """

            # Setting failed to False
            failed = False

            # Resetting wait_time, in case it was changed by the "StaleElementReferenceException"
            wait_time = 1

            # Printing URL number
            print(URLs_df[URLs_df['URL'] == URL].index[0])

        except StaleElementReferenceException:
            # In case of an error in loading
            failed = True
            wait_time = 5

        except MaxRetryError:
            # In this case the page is probably not found
            failed = False

        finally:
            # Write DataFrame to csv file
            if data_df.shape[0] > 0:
                data_df.to_csv("../Medium_Data.csv", index=False)
            # Quit browser
            browser.quit()
