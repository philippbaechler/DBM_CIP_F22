#!/usr/bin/env python3
'''Downloads all articles from www.reuters.com/news/archive and saves them as html files.

Usage:
    $ python3 01_download_articles_html.py
    or 
    $ chmod +x 01_download_articles_html.py
    $ ./01_download_articles_html.py

Author:
    Philipp Bächler - 22.5.2022

License:
    "THE BEER-WARE LICENSE" (Revision 42):
    philipp.baechler@gmail.com wrote this file. As long as you retain this notice
    you can do whatever you want with this stuff. If we meet some day, and you 
    think this stuff is worth it, you can buy me a beer in return.
'''


# %%
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


# %%
# Load the table wich contains all the article urls.
all_links = pd.read_csv("../data/all_links.csv", index_col=0)
print(len(all_links))
all_links.head()


# %%
# Specify the user agent
user_agent = (
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0)'
    ' Gecko/20100101 Firefox/81.0'
)

headers = {'User-Agent': user_agent}


# %%
# For collecting all article htmls we simply loop over the all_links table.
# With request we can get the html file of the desired page. This html file
# is then parsed and prettified with BeautifulSoup. Finally the document is
# saved as html file. As name we use a part of the url which seems to be 
# unique for each article. 

for idx, url in enumerate(all_links["url"]):
    print(idx)
    raw_html = requests.get(url, headers=headers)
    soup = bs(raw_html.content, "html.parser")
    html_page = soup.prettify()
    file_path = "../data/raw/reuters/" + url.split("/")[-1] + ".html"
    file = open(file_path, "w+")
    file.write(html_page)
    file.close()



# %%
