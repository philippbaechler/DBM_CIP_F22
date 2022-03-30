# %%
import re
import pandas as pd
import glob
from helper_converter import *


# %%
path_to_data = "data/raw/bild/2020/1"
articles_html = [f for f in glob.glob(path_to_data + "/**/*.html", recursive=True)]
print(len(articles_html))


# %%
def get_key_words(html_file):
    search_string = 'name="keywords" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('>', start_idx)
    return html_file[start_idx:end_idx].split("\"")[0].split(",")


def get_title(html_file):
    search_string = 'property="og:title" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('>', start_idx)
    return html_file[start_idx:end_idx].split("\"")[0].replace("\n", "")


def get_authors(html_file):
    search_string = 'class="authors__name">'
    start_idx = html_file.find(search_string) + len(search_string)
    if (start_idx <= len(search_string)):
        return []
    else:
        end_idx = html_file.find('</span>', start_idx)
        reporters = html_file[start_idx:end_idx]
        return re.split(', | und ', reporters)


def get_article_date_time(html_file):
    search_string = 'class="authors__pubdate"'
    start_idx = html_file.find(search_string) + len(search_string)
    if start_idx > len(search_string):
        start_idx = html_file.find('>', start_idx) + len('>')
        end_idx = html_file.find('</time>', start_idx)
        return pd.to_datetime(html_file[start_idx:end_idx].split(" Uhr")[0])
    else:
        search_string = 'class="datetime datetime--article"'
        start_idx = html_file.find(search_string) + len(search_string)
        if start_idx > len(search_string):
            start_idx = html_file.find('>', start_idx) + len('>')
            end_idx = html_file.find('</time>', start_idx)
            return pd.to_datetime(html_file[start_idx:end_idx].split(" Uhr")[0])
        else:
            search_string = '"publicationDate" : "'
            start_idx = html_file.find(search_string) + len(search_string)
            if start_idx > len(search_string):
                end_idx = html_file.find('",', start_idx)
                return pd.to_datetime(html_file[start_idx:end_idx])
            return pd.NA


def get_url(html_file):
    search_string = 'property="og:url" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    if start_idx > len(search_string):
        end_idx = html_file.find('"', start_idx)
        return html_file[start_idx:end_idx]
    else:
        return pd.NA


def get_description(html_file):
    search_string = 'name="description" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('"', start_idx)
    return html_file[start_idx:end_idx].replace("\n", "")


def get_paragraphs(html_file):
    paragraphs = re.findall(r"<p>(.*?)</p>", html_file)[1:]
    paragraphs = [remove_html_content(paragraph) for paragraph in paragraphs]
    return paragraphs


def get_topics(url):
    if not pd.isna(url):
        return article_url.replace("bild-plus/", "").split("/")[5]
    else:
        return pd.NA


def get_article_id(url):
    if not pd.isna(url):
        return re.findall(r"-([0-9]+).bild", article_url)[0]
    else:
        return pd.NA


# %%
articles = []

for article in articles_html:
    with open(article) as data:
        text_raw = data.read()
        text_raw = fix_unknown_characters(text_raw)
        key_words = get_key_words(text_raw)
        title = get_title(text_raw)
        reporters = get_authors(text_raw)
        article_date_time = get_article_date_time(text_raw)
        article_url = get_url(text_raw)
        description = get_description(text_raw)
        topic = get_topics(article_url)
        paragraphs = get_paragraphs(text_raw)
        article_id = get_article_id(article_url)
        articles.append({"article_date_time": article_date_time, "title": title, "description": description, \
                         "article_id": article_id, "reporters": reporters, "topic": topic, \
                         "key_words": key_words, "paragraphs": paragraphs, "url": article_url})
        

# %%
df = pd.DataFrame(articles)
df = df.astype(str).drop_duplicates().reset_index(drop=True)
df.head(10)


# %%
df.to_csv("data/output/bild_Jan_2020.csv")


# %%
