# %%
from selenium import webdriver
from selenium.webdriver.common.by import By


# max page: page=3277


# %%
def get_driver():
    driver = webdriver.Chrome()
    url = 'https://www.reuters.com/news/archive'
    driver.get(url)
    driver.get(url)
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    return driver


def get_articles_from_page(driver, url):
    driver.get(url)
    articles = driver.find_elements(By.TAG_NAME, "article")
    for article in articles:
        print(article.find_element(By.CLASS_NAME, "story-content").find_element(By.TAG_NAME, "a").get_attribute("href"))


# %%
driver = get_driver()


# %%
for idx in range(5):
    url = f'https://www.reuters.com/news/archive?view=page&page={idx}&pageSize=10'
    get_articles_from_page(driver, url)


# %%
