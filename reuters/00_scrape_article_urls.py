#!/usr/bin/env python3
'''Collects all article URLs from www.reuters.com/news/archive and saves them on the table "all_links.csv".

Usage:
    $ python3 00_scrape_article_urls.py
    or 
    $ chmod +x 00_scrape_article_urls.py
    $ ./00_scrape_article_urls.py

Author:
    Philipp Bächler - 22.5.2022

License:
    "THE BEER-WARE LICENSE" (Revision 42):
    philipp.baechler@gmail.com wrote this file. As long as you retain this notice
    you can do whatever you want with this stuff. If we meet some day, and you 
    think this stuff is worth it, you can buy me a beer in return.
'''


# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time


# %%
# We can add a --headless option to let the scraper work in the background
opts = webdriver.ChromeOptions()
#opts.add_argument('--headless')


# %%
def get_driver():
    driver = webdriver.Chrome(options=opts)
    url = 'https://www.reuters.com/news/archive'
    driver.get(url)
    time.sleep(5)
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    return driver


def get_articles_from_page(driver, url):
    driver.get(url)
    articles = driver.find_elements(By.TAG_NAME, "article")
    links = []
    for article in articles:
        links.append(article.find_element(By.CLASS_NAME, "story-content")\
                            .find_element(By.TAG_NAME, "a")\
                            .get_attribute("href"))
    return links


# %%
driver = get_driver()


# %%
# The reuters archive pages can be easily accessed by increasing the idx. 
# If we e.g. want to open page 10 -> replace idx with 10. The highest page 
# number (farthest back in time) is page 3277. On each page, we collect all
# article urls and save them in a list.

all_links = []
for idx in range(1789, 1793, 1):
    if idx % 100 == 0:
        driver.close()
        driver = get_driver()
    url = f'https://www.reuters.com/news/archive?view=page&page={idx}&pageSize=10'
    all_links.extend(get_articles_from_page(driver, url))


# %%
driver.close()

# %%
# Convert the all_links list into an pandas dataframe.
df = pd.DataFrame({"url": all_links})
df = df.drop_duplicates().reset_index(drop=True)
df.head()


# %%
# Save the dataframe in a csv.
df.to_csv("../data/all_links.csv")


# %%
