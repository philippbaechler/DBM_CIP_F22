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
df = pd.read_csv("data/output/reuters_dirty.csv", index_col=0, \
                 converters={"key_words": convert_string_to_list, \
                             "main_author": convert_string_to_list, \
                             "reporters": convert_string_to_list, \
                             "writers": convert_string_to_list, \
                             "editors": convert_string_to_list})
df.head(5)


# %%
# Check for data types
df.dtypes


# %%
# Convert to datetime to sort articles
df["article_date_time"] = pd.to_datetime(df["article_date_time"])
df.head()


# %%
# Check for missing datetimes
len(df[df["article_date_time"].isnull()])
len(df)


# %%
# As we have only three missing lines in 40991 observations, we simply delete these
df = df[df["article_date_time"].notnull()]


# %%
# Sort articles by datetime
df.sort_values(by="article_date_time", inplace=True)
df.reset_index(inplace=True, drop=True)
df.head()


# %%
# example keywords before 2021-04-08
df.iloc[24161]["key_words"]


# %%
# example keywords after 2021-04-09
df.iloc[24180]["key_words"]


# %%
# Restrict to articles before '2021-04-08'
df_sub = df[df["article_date_time"] < '2021-04-08']
df_sub.tail()


# %%
df_sub = df_sub.head(100)


# %%
articles = []           # id | date_time | title | description
article_keyword = []    # article_id | key_word_id
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
        article_keyword.append({"article_id": article_id, "keyword_id": int(keyword_id)})

    for main_author in row[1]["main_author"]:
        if main_author == "":
            continue
        role_id = df_roles.loc[df_roles["role"]=="main_author"]["id"]
        append_author_article_role(main_author, role_id, article_id)

    for reporter in row[1]["reporters"]:
        if reporter == "":
            continue
        role_id = df_roles.loc[df_roles["role"]=="reporter"]["id"]
        append_author_article_role(reporter, role_id, article_id)

    for writer in row[1]["writers"]:
        if writer == "":
            continue
        role_id = df_roles.loc[df_roles["role"]=="writer"]["id"]
        append_author_article_role(writer, role_id, article_id)

    for editor in row[1]["editors"]:
        if editor == "":
            continue
        role_id = df_roles.loc[df_roles["role"]=="editor"]["id"]
        append_author_article_role(editor, role_id, article_id)


df_articles = pd.DataFrame(articles)
df_article_keyword = pd.DataFrame(article_keyword)

df_keywords["id"] = df_keywords["id"].astype(int)
df_authors["id"] = df_authors["id"].astype(int)
df_article_author["article_id"] = df_article_author["article_id"].astype(int)
df_article_author["author_id"] = df_article_author["author_id"].astype(int)
df_author_role["author_id"] = df_author_role["author_id"].astype(int)
df_author_role["role_id"] = df_author_role["role_id"].astype(int)


# %%
df_keywords.to_csv("data/output/normalized/keywords.csv")
df_articles.to_csv("data/output/normalized/articles.csv")
df_article_keyword.to_csv("data/output/normalized/article_keyword.csv")
df_authors.to_csv("data/output/normalized/authors.csv")
df_article_author.to_csv("data/output/normalized/article_author.csv")
df_author_role.to_csv("data/output/normalized/author_role.csv")
df_roles.to_csv("data/output/normalized/roles.csv")


# %%
