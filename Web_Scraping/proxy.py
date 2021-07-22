# Importing needed packages
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time

# Defining needed variables
URL = 'https://free-proxy-list.net/'
proxies = list()


def get_proxies():
    """
    Get a list of proxies
    :return proxies: a list containing 20 proxies
    """
    # Setting up Firefox
    options = Options()
    options.headless = True
    options.add_argument("--disable-extensions")
    browser = webdriver.Firefox(options=options)
    time.sleep(5)  # Wait for browser to open
    browser.get(URL)

    def get_table():
        """
        Get Proxies list in page
        """
        # Sort elements by https
        sort_https = browser.find_element_by_xpath("//th[@aria-label='Https: activate to sort column ascending']")
        sort_https.click()
        sort_https.click()

        # Getting table
        table = browser.find_element_by_xpath("//table[@aria-describedby='proxylisttable_info']")

        # Getting td elements
        tds = table.find_elements_by_tag_name('td')

        # Getting IP Address and Port
        for i in range(0, len(tds) - 1, 8):
            # Each row has 8 elements we only want the first 2
            ip = tds[i].text
            port = tds[i + 1].text

            # Getting Proxy
            proxy = {
                "http": 'http://' + ip + ':' + port,
                "https": 'https://' + ip + ':' + port
            }

            # Appending proxy to proxies list
            proxies.append(proxy)

    # Getting proxies in the first page
    get_table()

    # Going to the next page
    next_page = browser.find_element_by_xpath("//*[@id='proxylisttable_next']/a")
    next_page.click()

    # Getting proxies in the second page
    get_table()

    # Close browser
    browser.quit()

    return proxies


# Write proxies to csv file
proxies_series = pd.Series(get_proxies())
proxies_series.to_csv("proxies.csv", header=["Proxy"], index=False)
