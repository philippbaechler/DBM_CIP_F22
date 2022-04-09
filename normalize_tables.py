# %%
import pandas as pd
import numpy as np


# %%
def convert_string_to_list(string_input):
    return string_input.replace("'", "")\
                       .replace("[", "")\
                       .replace("]", "")\
                       .split(", ")


# %%
df = pd.read_csv("data/output/reuters_sample_unnormalized.csv", index_col=0, \
                 converters={"key_words": convert_string_to_list})
df.sample(5)


# %%
df_sub = df[["article_date_time", "title", "description", "key_words"]]
df_sub


# %%
articles = []    # id | date_time | title | description
describes = []   # article_id | key_word_id
df_keywords = pd.DataFrame({"id": [], "keyword": []})   # id | key_word
#keyword_ids = []

cntr = 0

for row in df_sub.iterrows():
    if cntr % 100 == 0:
        print(cntr)
    cntr += 1
    article_id = row[0]
    article_title = row[1]["title"]
    article_date_time = row[1]["article_date_time"]
    article_description = row[1]["description"]
    all_article_description = row[1]["description"]
    articles.append({"id": article_id, "date_time": article_date_time, \
                     "title": article_title, "description": article_description})
    all_article_keywords = row[1]["key_words"]
    for keyword in all_article_keywords:
        if keyword not in list(df_keywords["keyword"]):
            keyword_id = len(df_keywords)
            df_keywords = df_keywords.append({"id": keyword_id, "keyword": keyword}, ignore_index=True)
        keyword_id = df_keywords.loc[df_keywords["keyword"] == keyword]["id"]
        describes.append({"article_id": article_id, "keyword_id": int(keyword_id)})


df_keywords["id"] = df_keywords["id"].astype(int)
print(df_keywords.sample(5))

df_articles = pd.DataFrame(articles)
print(df_articles.sample(5))

df_describes = pd.DataFrame(describes)
print(df_describes.sample(5))

# %%
df_keywords.to_csv("data/output/keywords.csv")
df_articles.to_csv("data/output/articles.csv")
df_describes.to_csv("data/output/describes.csv")


# %%
