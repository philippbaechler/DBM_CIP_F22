#%%
import os
import re
import pandas as pd
import glob
from bs4 import BeautifulSoup as bs
from helper_converter import *


#%%
curren_dir = os.path.abspath(os.getcwd())
path_to_data = "data/raw/reuters/"
articles_html = [f for f in glob.glob(path_to_data + "**/**/*.html", recursive=True)]
print(len(articles_html))


#%%
def get_key_words(article_soup):
    try:
        return article_soup.find("meta", attrs={'name':'keywords'}).attrs["content"].split(",")
    except:
        return []


def get_title(article_soup):
    try:
        return article_soup.find("meta", attrs={'name':'analyticsAttributes.title'}).attrs["content"]
    except:
        return ""
    

def get_article_date_time(article_soup):
    try:
        return pd.to_datetime(article_soup.find("meta", attrs={'name':'analyticsAttributes.articleDate'}).attrs["content"])
    except:
        return ""


def get_main_authors(article_soup):
    try:
        return article_soup.find("meta", attrs={'name':'analyticsAttributes.author'}).attrs["content"].split(",")
    except:
        return ""


def get_reporters_writers_and_editors(article_soup):
    try:
        substrings = article_soup.find("div", class_='Attribution-attribution-Y5JpY').find("p").get_text().split(";")
        reporters = []
        editors = []
        writers = []
        for substring in substrings:
            reporter = re.split('[eE]diting by', substring)[0]
            reporter = re.findall(r"[rR]eporting\sby\s(.*)", reporter)
            if len(reporter) != 0:
                reporters.append(re.split(' and | & |, ', reporter[0]))
            editor = re.findall(r"[eE]diting\sby\s(.*)", substring)
            if len(editor) != 0:
                editors.append(re.split(' and | & |, ', editor[0]))
            writer = re.split('[eE]diting by', substring)[0]
            writer = re.findall(r"[wW]riting\sby\s(.*)", writer)
            if len(writer) != 0:
                writers.append(re.split(' and | & |, ', writer[0]))
        return sum(reporters, []), sum(writers, []), sum(editors, [])
    except:
        return [],[],[]


def get_url(article_soup):
    try:
        return article_soup.find("meta", attrs={'name':'analyticsAttributes.canonicalUrl'}).attrs["content"]
    except:
        return ""


def get_contentChannel(article_soup):
    try:
        return article_soup.find("meta", attrs={'name':'analyticsAttributes.topicChannel'}).attrs["content"]
    except:
        return ""


def get_description(article_soup):
    try:
        return article_soup.find("meta", attrs={'name':'description'}).attrs["content"]
    except:
        return ""


def get_paragraphs_and_location(article_soup):
    paragraphs = article_soup.find_all("p", class_="Paragraph-paragraph-2Bgue ArticleBody-para-TD_9x")
    paragraphs = [paragraph.get_text() for paragraph in paragraphs]
    paragraphs = [remove_html_content(paragraph) for paragraph in paragraphs]
    paragraphs = [paragraph.replace("\n         ", "") for paragraph in paragraphs]
    paragraphs = [paragraph.replace("\n        ", "") for paragraph in paragraphs]
    location = ""
    if len(paragraphs) > 0:
        para_split = paragraphs[0].split("(Reuters) - ")
        if len(para_split) > 1:
            location = para_split[0]
            paragraphs[0] = para_split[1]
    return paragraphs, location 


def get_article_id(article_url):
    return article_url.split("-id")[-1]


# %%
articles = []

for idx, article in enumerate(articles_html):
    if idx >= 120:
        break
    with open(article) as data:
        data = data.read()
        data = fix_unknown_characters(data)
        soup = bs(data, 'html.parser')
        key_words = get_key_words(soup)
        title = get_title(soup)
        article_date_time = get_article_date_time(soup)
        main_author = get_main_authors(soup)
        reporters, writers, editors = get_reporters_writers_and_editors(soup)
        article_url = get_url(soup)
        content_channel = get_contentChannel(soup)
        description = get_description(soup)
        paragraphs, location = get_paragraphs_and_location(soup)
        article_text = join_paragraphs_to_text(paragraphs)
        article_id = get_article_id(article_url)
        articles.append({"article_date_time": article_date_time, "title": title, "description": description, \
                         "article_id": article_id, "main_author": main_author, "reporters": reporters, \
                         "writers": writers, "editors": editors, "content_channel": content_channel, \
                         "key_words": key_words, "location": location, "text": article_text, "url": article_url})


# %%
df = pd.DataFrame(articles)
df = df.astype(str).drop_duplicates().reset_index(drop=True)
df.head(10)


# %%
df.to_csv("data/output/reuters_Jan_2020.csv")


# %%
