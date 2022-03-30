#%%
import os
import re
import pandas as pd
import glob
from helper_converter import *


#%%
curren_dir = os.path.abspath(os.getcwd())
path_to_data = "data/raw/reuters/2020/1"
articles_html = [f for f in glob.glob(path_to_data + "**/**/*.html", recursive=True)]
print(len(articles_html))


#%%
def get_key_words(html_file):
    search_string = 'name="keywords" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('" />', start_idx)
    return html_file[start_idx:end_idx].split(",")


def get_title(html_file):
    search_string = 'name="analyticsAttributes.title" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('" />', start_idx)
    return html_file[start_idx:end_idx]


def get_article_date_time(html_file):
    search_string = 'name="analyticsAttributes.articleDate" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('" />', start_idx)
    return pd.to_datetime(html_file[start_idx:end_idx])


def get_main_author(html_file):
    search_string = 'name="Author" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('">', start_idx)
    return html_file[start_idx:end_idx]


def get_reporters_writers_and_editors(html_file):
    search_string = '<p class="Attribution_content">'
    start_idx = html_file.find(search_string) + len(search_string)
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
    return html_file[start_idx:end_idx]


def get_contentChannel(html_file):
    search_string = 'name="analyticsAttributes.topicChannel" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('" />', start_idx)
    return html_file[start_idx:end_idx]


def get_description(html_file):
    search_string = 'name="description" content=\''
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('\' />', start_idx)
    return html_file[start_idx:end_idx]


def get_paragraphs(html_file):
    paragraphs = re.findall(r"<p>(.*?)</p>", html_file)
    paragraphs = [remove_html_content(paragraph) for paragraph in paragraphs]
    return paragraphs


def get_article_id(html_file):
    search_string = 'data-scrolltoid="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('"', start_idx)
    return html_file[start_idx:end_idx]


# %%
articles = []

for article in articles_html:
    with open(article) as data:
        text_raw = data.read()
        text_raw = fix_unknown_characters(text_raw)
        key_words = get_key_words(text_raw)
        title = get_title(text_raw)
        article_date_time = get_article_date_time(text_raw)
        main_author = get_main_author(text_raw)
        reporters, writers, editors = get_reporters_writers_and_editors(text_raw)
        article_url = get_url(text_raw)
        content_channel = get_contentChannel(text_raw)
        description = get_description(text_raw)
        paragraphs = join_paragraphs_to_text(get_paragraphs(text_raw))
        article_id = get_article_id(text_raw)
        articles.append({"article_date_time": article_date_time, "title": title, "description": description, \
                         "article_id": article_id, "main_author": main_author, "reporters": reporters, \
                         "writers": writers, "editors": editors, "content_channel": content_channel, \
                         "key_words": key_words, "paragraphs": paragraphs, "url": article_url})


# %%
df = pd.DataFrame(articles)
df = df.astype(str).drop_duplicates().reset_index(drop=True)
df.head(10)


# %%
df.to_csv("data/output/reuters_Jan_2020.csv")


# %%
