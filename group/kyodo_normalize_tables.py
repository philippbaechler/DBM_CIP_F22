# %%
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt


# %%
def convert_string_to_list(string_input):
    return string_input.replace("'", "")\
                       .replace("[", "")\
                       .replace("]", "")\
                       .split(", ")


# %%
df_kyodo = pd.read_csv("../data/output/kyodo_src.csv", \
                 converters={"channels": convert_string_to_list, \
                             "keywords": convert_string_to_list, \
                             "author": convert_string_to_list})
df_kyodo["datetime"] = pd.to_datetime(df_kyodo["datetime"])
df_kyodo["paragraph"] = df_kyodo["paragraph"].str.replace("[", "").str.replace("]", "")
df_kyodo = df_kyodo.rename(columns={"paragraph": "text"})
df_kyodo.sort_values(by="datetime", inplace=True)
df_kyodo.reset_index(inplace=True, drop=True)
df_kyodo.head(3)


# %%
df_kyodo = df_kyodo.head(500)

# %%
df_articles = pd.read_csv("../data/output/normalized/reuters/articles.csv", index_col=0)
df_article_keyword = pd.read_csv("../data/output/normalized/reuters/article_keyword.csv", index_col=0)
df_keywords = pd.read_csv("../data/output/normalized/reuters/keywords.csv", index_col=0)
df_authors = pd.read_csv("../data/output/normalized/reuters/authors.csv", index_col=0)
df_article_author = pd.read_csv("../data/output/normalized/reuters/article_author.csv", index_col=0)
df_roles = pd.read_csv("../data/output/normalized/reuters/roles.csv", index_col=0)

# %%

cntr = 0

for row in df_kyodo.iterrows():
    if cntr % 100 == 0:
        print(cntr)
    cntr += 1

    article_id = row[0]
    article_title = row[1]["title"]
    article_date_time = row[1]["datetime"]
    article_description = row[1]["description"]
    article_text = row[1]["text"]
    article_url = row[1]["url"]
    df_articles = df_articles.append({"id": article_id, "datetime": article_date_time, \
                                      "title": article_title, "description": article_description, \
                                      "text": article_text, "url": article_url}, ignore_index=True)
    all_article_keywords = row[1]["keywords"]

    for keyword in all_article_keywords:
        if keyword not in list(df_keywords["keyword"]):
            keyword_id = len(df_keywords)
            df_keywords = df_keywords.append({"id": keyword_id, "keyword": keyword}, ignore_index=True)
        keyword_id = df_keywords.loc[df_keywords["keyword"]==keyword]["id"]
        df_article_keyword = df_article_keyword.append({"article_id": article_id, \
                                                        "keyword_id": int(keyword_id)}, ignore_index=True)


# %%



