# %%
import os
import re
import pandas as pd
import glob

# %%
path_to_data = "data/raw/aljazeera/2020/2/2"
articles_html = [f for f in glob.glob(path_to_data + "/**/*.html", recursive=True)]
print(len(articles_html))


#%%
def fix_unknown_characters(string_input):
    string_input = string_input.replace("&#039;", "'")
    string_input = string_input.replace("&#39;", "'")
    string_input = string_input.replace("&quot;", "\"")
    string_input = string_input.replace("&rsquo;", "’")
    string_input = string_input.replace("&lsquo;", "‘")
    string_input = string_input.replace("&rdquo;", "”")
    string_input = string_input.replace("&ldquo;", "“")
    string_input = string_input.replace("&amp;", "&")
    string_input = string_input.replace("\xa0", " ")
    return string_input


def remove_html_content(string_input):
    html_contents = re.findall(r"<(.*?)>", string_input)
    for content in html_contents:
        string_input = string_input.replace(("<" + content + ">"), "")
    return string_input


def get_key_words(html_file):
    search_string = 'name="news_keywords" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('">', start_idx)
    return html_file[start_idx:end_idx].split(",")


def get_title(html_file):
    search_string = 'name="title" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('">', start_idx)
    return html_file[start_idx:end_idx]


def get_article_date_time(html_file):
    search_string = 'class="article-heading-author-wrap"'
    start_idx = html_file.find(search_string) + len(search_string)
    search_string = 'class="timeagofunction"'
    start_idx = html_file.find(search_string, start_idx) + len(search_string)
    start_idx = html_file.find(">", start_idx) + len(">")
    end_idx = html_file.find('</time>', start_idx)
    return pd.to_datetime(html_file[start_idx:end_idx].split(" GMT")[0])


def get_main_author(html_file):
    search_string = 'class="article-heading-author-wrap"'
    start_idx = html_file.find(search_string) + len(search_string)
    search_string = 'rel="author"'
    start_idx = html_file.find(search_string, start_idx) + len(search_string)
    if (start_idx <= len(search_string)):
        return pd.NA
    else:
        start_idx = html_file.find('">', start_idx) + len('">')
        end_idx = html_file.find('</a>', start_idx)
        return html_file[start_idx:end_idx]


def get_url(html_file):
    search_string = 'name="url" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('">', start_idx)
    return html_file[start_idx:end_idx]


def get_description(html_file):
    search_string = 'name="description" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('">', start_idx)
    return html_file[start_idx:end_idx]


def get_topics(html_file):
    topics = re.findall(r"data-topic-name=\"(.*?)\">", html_file)
    return topics


def get_paragraphs(html_file):
    paragraphs = re.findall(r"<p>(.*?)</p>", html_file)
    paragraphs = [remove_html_content(paragraph) for paragraph in paragraphs]
    return paragraphs


def get_article_id(html_file):
    search_string = 'name="guid" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('">', start_idx)
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
        article_url = get_url(text_raw)
        description = get_description(text_raw)
        topics = get_topics(text_raw)
        paragraphs = get_paragraphs(text_raw)
        article_id = get_article_id(text_raw)
        articles.append({"article_date_time": article_date_time, "title": title, "description": description, \
                         "article_id": article_id, "main_author": main_author, "topics": topics, \
                         "key_words": key_words, "paragraphs": paragraphs, "url": article_url})


# %%
df = pd.DataFrame(articles)
df = df.astype(str).drop_duplicates().reset_index(drop=True)
df.head(10)


# %%
df.to_csv("data/output/al_jazeera_Feb_2020.csv")

