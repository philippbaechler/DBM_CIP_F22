# %%
import re
import pandas as pd
import glob


# %%
path_to_data = "data/raw/bild/2020/1/1"
articles_html = [f for f in glob.glob(path_to_data + "/**/*.html", recursive=True)]
print(len(articles_html))


# %%
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
    end_idx = html_file.find('" />', start_idx)
    return html_file[start_idx:end_idx].split(",")


def get_title(html_file):
    search_string = 'property="og:title" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    end_idx = html_file.find('"/>', start_idx)
    return html_file[start_idx:end_idx]


def get_authors(html_file):
    search_string = 'class="authors__name">'
    start_idx = html_file.find(search_string) + len(search_string)
    if (start_idx <= len(search_string)):
        return pd.NA
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
        return html_file[start_idx:end_idx].split(" Uhr")[0]
    else:
        return pd.NA


def get_url(html_file):
    search_string = 'property="og:url" content="'
    start_idx = html_file.find(search_string) + len(search_string)
    if start_idx > len(search_string):
        end_idx = html_file.find('"', start_idx)
        return html_file[start_idx:end_idx]
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





# %%
