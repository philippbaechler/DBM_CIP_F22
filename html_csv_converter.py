#%%
import os
from os import listdir
from os.path import join
import re
from numpy import empty
import pandas as pd


#%%
curren_dir = os.path.abspath(os.getcwd())
path_to_data = "data/raw/reuters/17"
articles_html = listdir(path_to_data)


#%%
def get_key_words(html_file):
    start_idx = html_file.find('name="keywords" content="') + len('name="keywords" content="')
    end_idx = html_file.find('" />', start_idx)
    return html_file[start_idx:end_idx].split(",")


def get_title(html_file):
    start_idx = html_file.find('name="analyticsAttributes.title" content="') + len('name="analyticsAttributes.title" content="')
    end_idx = html_file.find('" />', start_idx)
    return html_file[start_idx:end_idx].replace("&#039;", "'")


def get_article_date_time(html_file):
    start_idx = html_file.find('name="analyticsAttributes.articleDate" content="') + len('name="analyticsAttributes.articleDate" content="')
    end_idx = html_file.find('" />', start_idx)
    return pd.to_datetime(html_file[start_idx:end_idx])


def get_main_author(html_file):
    start_idx = html_file.find('name="Author" content="') + len('name="Author" content="')
    end_idx = html_file.find('">', start_idx)
    return html_file[start_idx:end_idx]

def get_reporters_writers_and_editors(html_file):
    start_idx = html_file.find('<p class="Attribution_content">') + len('<p class="Attribution_content">')
    end_idx = html_file.find('</p>', start_idx)
    substrings = html_file[start_idx:end_idx].split(";")
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


def get_url(html_file):
    search_string = 'name="analyticsAttributes.canonicalUrl" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('" />', start_idx)
    substring = html_file[start_idx:end_idx]
    return substring


# %%
articles = []

for article in articles_html:
    with open(join(path_to_data, article, "source.html")) as data:
        text_raw = data.read()
        key_words = get_key_words(text_raw)
        title = get_title(text_raw)
        article_date_time = get_article_date_time(text_raw)
        main_author = get_main_author(text_raw)
        reporters, writers, editors = get_reporters_writers_and_editors(text_raw)
        article_url = get_url(text_raw)
        articles.append({"key_words": key_words, "title": title, "article_date_time": article_date_time,\
                         "main_author": main_author, "reporters": reporters, "writers": writers, \
                         "editors": editors, "url": article_url})



# %%
df = pd.DataFrame(articles)
df.head(10)


# %%
df.to_csv("data/output/test.csv")


# %%
