# %%
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
import pytz
from analysis_helper import *


# %%
df_kyodo = pd.read_csv("../data/output/kyodo_src.csv", \
                 converters={"channels": convert_string_to_list, \
                             "keywords": convert_string_to_list, \
                             "author": convert_string_to_list})

df_kyodo["datetime"] = pd.to_datetime(df_kyodo["datetime"])
df_kyodo["datetime"] = df_kyodo["datetime"].dt.tz_localize(pytz.timezone('Asia/Tokyo'))
df_kyodo["paragraph"] = df_kyodo["paragraph"].str.replace("[", "").str.replace("]", "")
df_kyodo = df_kyodo.rename(columns={"keywords": "key_words", "channels": "content_channel", "paragraph": "text", "datetime": "article_date_time", "author": "authors"})
df_kyodo["publisher"] = "Kyodo News"
df_kyodo.drop(columns=["authors"], inplace=True)
df_kyodo.head(3)


# %%
df_reuters = pd.read_csv("../data/output/reuters_dirty.csv", index_col=0, \
                 converters={"key_words": convert_string_to_list, \
                             "main_author": convert_string_to_list, \
                             "reporters": convert_string_to_list, \
                             "writers": convert_string_to_list, \
                             "editors": convert_string_to_list})

df_reuters["article_date_time"] = pd.to_datetime(df_reuters["article_date_time"])
df_reuters = df_reuters[df_reuters["article_date_time"].notnull()]
df_reuters["publisher"] = "Thompson and Reuters"
df_reuters.head(3)


# %%
df_combined = df_kyodo.append(df_reuters)
df_combined.sort_values(by="article_date_time", inplace=True)
df_combined.reset_index(inplace=True, drop=True)
df_combined["year_month"] = [datetime(year=d.year, month=d.month, day=1) for d in df_combined["article_date_time"]]
df_combined.head()


# %%
df_combined.to_csv("../data/output/combined_src.csv")


# %%
