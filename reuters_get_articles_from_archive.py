# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
# max page: page=3277

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
        links.append(article.find_element(By.CLASS_NAME, "story-content").find_element(By.TAG_NAME, "a").get_attribute("href"))
    return links


# %%
driver = get_driver()


# %%
all_links = []

for idx in range(2000, 2010, 1):
    if idx % 100 == 0:
        driver.close()
        driver = get_driver()
    url = f'https://www.reuters.com/news/archive?view=page&page={idx}&pageSize=10'
    all_links.extend(get_articles_from_page(driver, url))


# %%
df = pd.DataFrame({"url": all_links})
df.head()

# %%
df.shape

# %%
df = df.drop_duplicates().reset_index()
df.shape

# %%
df.to_csv("data/all_links.csv")

# %%
