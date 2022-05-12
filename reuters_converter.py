#%%
import os
import re
import pandas as pd
import glob
from bs4 import BeautifulSoup as bs
from helper_converter import *


#%%
curren_dir = os.path.abspath(os.getcwd())
path_to_data = "data/raw/reuters_old/1/"
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
        title = article_soup.find("meta", attrs={'name':'analyticsAttributes.title'})
        if title == None:
            title = article_soup.find("meta", attrs={'property':'og:title'})
        return title.attrs["content"]
    except:
        return ""
    

def get_article_date_time(article_soup):
    try:
        article_datetime = article_soup.find("meta", attrs={'name':'analyticsAttributes.articleDate'})
        if article_datetime == None:
            article_datetime = article_soup.find("meta", attrs={'name':'article:published_time'})
        return pd.to_datetime(article_datetime.attrs["content"])
    except:
        return ""


def get_main_authors(article_soup):
    try:
        author_names = article_soup.find("meta", attrs={'name':'analyticsAttributes.author'})
        if author_names == None:
            author_names = article_soup.find("meta", attrs={'name':'article:author'})
        return author_names.attrs["content"].split(",")
    except:
        return ""


def split_author_names(names):
    return re.split(' and |,and | amd | anf | And | & |, |,| ad |/| aboard ', names)


def get_reporters_writers_and_editors(article_soup):
    try:
        substrings = article_soup.find("body").get_text()
        substrings = re.split('\n|; |Our Standards', substrings)
        reporters = []
        editors = []
        writers = []
        
        for substring in substrings:
            if "reporting by" in substring.lower():
                reporter = re.findall(r"[rR]eporting\sby\s(.*)", substring)
                if len(reporter) != 0:
                    reporters.append(split_author_names(reporter[0]))
            elif "editing by" in substring.lower():
                editor = re.findall(r"[eE]diting\sby\s(.*)", substring)
                if len(editor) != 0:
                    editors.append(split_author_names(editor[0]))
            elif "writing by" in substring.lower():
                writer = re.findall(r"[wW]riting\sby\s(.*)", substring)
                if len(writer) != 0:
                    writers.append(split_author_names(writer[0]))
        return sum(reporters, []), sum(writers, []), sum(editors, [])
    except:
        return [],[],[]


def get_url(article_soup):
    try:
        article_url = article_soup.find("meta", attrs={'name':'analyticsAttributes.canonicalUrl'})
        if article_url == None:
            article_url = article_soup.find("meta", attrs={'property':'og:url'})
        return article_url.attrs["content"]
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


def get_paragraphs(article_soup):
    paragraphs = article_soup.find_all("p")
    if len(paragraphs) > 0:
        paragraphs = [paragraph.get_text() for paragraph in paragraphs]
        paragraphs = [remove_html_content(paragraph) for paragraph in paragraphs]
        paragraphs = [remove_new_line_character(paragraph) for paragraph in paragraphs]
        paragraphs = [re.sub("([ ]{2,})", "", paragraph) for paragraph in paragraphs]
        if "Min Read" in paragraphs[0]:
            paragraphs.pop(0)
        return paragraphs
    else:
        return []


def get_article_id(article_url):
    return article_url.split("-id")[-1].replace(".html", "")


# %%
articles = []

for idx, article in enumerate(articles_html):
    if idx >= 1000:
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
        paragraphs = get_paragraphs(soup)
        article_text = join_paragraphs_to_text(paragraphs)
        articles.append({"article_date_time": article_date_time, "title": title, "description": description, \
                         "main_author": main_author, "reporters": reporters, \
                         "writers": writers, "editors": editors, "content_channel": content_channel, \
                         "key_words": key_words, "text": article_text, "url": article_url})


# %%
df = pd.DataFrame(articles)
df = df.astype(str).drop_duplicates().reset_index(drop=True)
df.head(10)


# %%
df.to_csv("data/output/reuters_sample.csv")


# %%
