# %%
import pandas as pd
import numpy as np


# %%
def convert_string_to_list(string_input):
    return string_input.replace("'", "")\
                       .replace("[", "")\
                       .replace("]", "")\
                       .split(", ")


def append_author_article_role(name, role_id, article_id):
    global df_authors, df_article_author, df_author_role
    if name not in list(df_authors["name"]):
        df_authors = df_authors.append({"id":len(df_authors), "name":name}, ignore_index=True)
    author_id = df_authors.loc[df_authors["name"]==name]["id"]
    df_article_author = df_article_author.append({"article_id": int(article_id), "author_id": int(author_id)}, ignore_index=True)
    if not (df_author_role == np.array([int(author_id), int(role_id)])).all(1).any():
        df_author_role = df_author_role.append({"author_id":int(author_id), "role_id":int(role_id)}, ignore_index=True)


# %%
df = pd.read_csv("data/output/reuters_sample_unnormalized.csv", index_col=0, \
                 converters={"key_words": convert_string_to_list, \
                             "reporters": convert_string_to_list, \
                             "writers": convert_string_to_list, \
                             "editors": convert_string_to_list})
df.sample(5)


# %%
df_sub = df[["article_date_time", "title", "description", "key_words", \
             "main_author", "reporters", "writers", "editors"]]
df_sub


# %%
articles = []                                               # id | date_time | title | description
describes = []                                              # article_id | key_word_id
df_keywords = pd.DataFrame({"id":[], "keyword":[]})
df_authors = pd.DataFrame({"id":[], "name":[]})
df_article_author = pd.DataFrame({"article_id":[], "author_id":[]})
df_author_role = pd.DataFrame({"author_id":[], "role_id":[]})
df_roles = pd.DataFrame({"id":[0, 1, 2, 3], 
                         "role":["main_author", "reporter", "writer", "editor"]})
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
    articles.append({"id": article_id, "datetime": article_date_time, \
                     "title": article_title, "description": article_description})
    all_article_keywords = row[1]["key_words"]

    for keyword in all_article_keywords:
        if keyword not in list(df_keywords["keyword"]):
            keyword_id = len(df_keywords)
            df_keywords = df_keywords.append({"id": keyword_id, "keyword": keyword}, ignore_index=True)
        keyword_id = df_keywords.loc[df_keywords["keyword"]==keyword]["id"]
        describes.append({"article_id": article_id, "keyword_id": int(keyword_id)})

    if not pd.isna(row[1]["main_author"]):
        main_author_name = row[1]["main_author"]
        role_id = df_roles.loc[df_roles["role"]=="main_author"]["id"]
        append_author_article_role(main_author_name, role_id, article_id)


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
