#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 


#%%
driver = webdriver.Chrome()
url = 'https://www.reuters.com/world/americas/'
driver.get(url)
driver.implicitly_wait(4)
element = driver.find_element(By.ID, "onetrust-accept-btn-handler")
element.click()


#%%
for i in range(20):
    elements = driver.find_elements(by=By.XPATH, value=u"//button[contains(@class, 'button')]")

    for element in elements:
        if element.text=="Load More":
            new_height = driver.execute_script("return document.body.scrollHeight")
            print(i, new_height)
            driver.execute_script(f"window.scrollTo(0,{new_height-3500})")
            element.click()
            break
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script(f"window.scrollTo(0,{new_height-3500})")
new_height 
#%%
driver.execute_script("window.scrollTo(0,0)")
#%%
new_height = driver.execute_script("return document.body.scrollHeight")
driver.execute_script(f"window.scrollTo(0,{new_height-3500})")
#%%
new_height = driver.execute_script("return document.body.scrollHeight")
new_height

# %%
