# %%
import pandas as pd
import numpy as np
import re


# %%
df = pd.read_csv("data/output/reuters_Jan_2020.csv", index_col=0)
df.sample(5)


# %%
df_sub = df[["article_date_time", "title", "description", "key_words"]]
df_sub["key_words"] = df_sub.key_words.apply(lambda x: x[0:-1].replace("'", "").split(', '))
df_sub


# %%
articles = []    # article_id | date_time | title | description
describes = []   # article_id | key_word_id
df_keywords = pd.DataFrame({"keyword_id": [], "keyword": []})   # key_word_id | key_word
#keyword_ids = []
#%%
for row in df_sub.iterrows():
    article_id = row[0]
    article_title = row[1]["title"]
    article_date_time = row[1]["article_date_time"]
    article_description = row[1]["description"]
    all_article_description = row[1]["description"]
    articles.append({"article_id": article_id, "date_time": article_date_time, \
                     "title": article_title, "description": article_description})
    all_article_keywords = row[1]["key_words"]
    for keyword in all_article_keywords:
        if keyword not in list(df_keywords["keyword"]):
            keyword_id = (len(df_keywords))
            df_keywords = df_keywords.append({"keyword_id": keyword_id, "keyword": keyword}, ignore_index=True)
        keyword_id = df_keywords.loc[df_keywords["keyword"] == keyword]["keyword_id"]
        describes.append({"article_id": article_id, "keyword_id": keyword_id})



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
