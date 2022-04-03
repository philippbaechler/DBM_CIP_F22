# %%
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


# %%
all_links = pd.read_csv("data/all_links.csv", index_col=0)
all_links.head()


# %%
user_agent = (
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0)'
    ' Gecko/20100101 Firefox/81.0'
)

headers = {'User-Agent': user_agent}


# %%
for idx, url in enumerate(all_links["url"]):
    print(idx)
    raw_html = requests.get(url, headers=headers)
    soup = bs(raw_html.content, "lxml")
    html_page = soup.prettify()
    file_path = "data/raw/reuters/" + url.split("/")[-2] + ".html"
    file = open(file_path, "w+")
    file.write(html_page)
    file.close()



# %%
