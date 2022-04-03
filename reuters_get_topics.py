#%%
from selenium import webdriver
from selenium.webdriver.common.by import By


# %%
def get_driver():
    driver = webdriver.Chrome()
    url = 'https://www.reuters.com/'
    driver.get(url)
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    return driver


def get_main_categories(driver):
    elements = driver.find_elements(By.XPATH,u"//section[contains(@class, 'site-footer__link-group')]")
    a = []
    hrefs = []
    for el in elements:
        if el.find_element(By.TAG_NAME, "h3").text == "Browse":
            a = el.find_elements(By.TAG_NAME, "a")

    for el in a:
        hrefs.append(el.get_property("href"))

    return hrefs


def get_sub_categories_from_main_category(driver, url):
    print("main category:", url)
    driver.get(url)
    option_elements = driver.find_elements(By.TAG_NAME, "option")
    sub_categories = []
    for el in option_elements:
        url = "https://www.reuters.com" + el.get_attribute("value")
        sub_categories.append(url)
    return sub_categories


def get_all_article_links_from_sub_category(driver, url):
    print("sub category:", url)
    driver.get(url)
    li_elements = driver.find_elements(By.XPATH,u"//li[contains(@class, 'story-collection')]")
    article_links = []
    for el in li_elements:
        a_elements = el.find_elements(By.TAG_NAME, "a")
        for a in a_elements:
            article_links.append(a.get_attribute("href"))
    article_links = list(dict.fromkeys(article_links))
    return article_links    

    
#%%
driver = get_driver()

#%%
main_categories = get_main_categories(driver)

# %%
sub_categories = get_sub_categories_from_main_category(driver, main_categories[0])

# %%
get_all_article_links_from_sub_category(driver, sub_categories[3])

# %%
