# #
# This script will clean the previously 'dirtified' data scraped from Yahooo Finance.
# These cleaned data is then stored in a single table: data/output/clean/ Yahoo_BTC_src_stage.csv
#
# The following Errors are considered:
# - duplicated entries
# - missing Date entry
# - missing rows
# - outlier detection and correction
#
# #

# %%
import numpy as np
import pandas as pd
from functools import reduce
import os

# %% set pandas  options
pd.set_option('display.max_columns', 0)  # Display any number of columns
pd.set_option('display.max_rows', 0)  # Display any number of rows
pd.set_option('expand_frame_repr', False)

# %%
# Loading of dataset. Load empty dataset if File not found
file = 'Yahoo_BTC_src_dirty.csv'

# %% load data
df_bitcoin = pd.read_csv("../data/output/clean/Yahoo_BTC_src_stage.csv", index_col='Date',
                         parse_dates=True,
                         infer_datetime_format=True)
df_kyodo_articles = pd.read_csv("../data/output/normalized_stage/Kyodo_articles_cleaned.csv", index_col=0,
                                parse_dates=True,
                                infer_datetime_format=True)

df_reuters_articles = pd.read_csv("../data/output/normalized_stage/articles.csv", index_col=0,
                                  parse_dates=True,
                                  infer_datetime_format=True)
df_reuters_article_keyword = pd.read_csv("../data/output/normalized_stage/article_keyword.csv", index_col=0)
df_reuters_keyword = pd.read_csv("../data/output/normalized_stage/keywords.csv", index_col=0)


df_kyodo_articles["Date"] = pd.to_datetime(df_kyodo_articles['datetime']).dt.normalize() # convert Date column items to datetime.date
df_kyodo_articles.set_index('Date', inplace=True) # set Date as row index
df_kyodo_articles.drop('datetime', axis=1, inplace=True)
df_kyodo_articles.sort_index(inplace=True)

df_reuters = df_reuters_articles.merge(df_reuters_article_keyword, how='left', left_on='id', right_on='article_id')
df_reuters = df_reuters.merge(df_reuters_keyword, how='left', left_on='keyword_id', right_on='id')

df_reuters_articles["Date"] = pd.to_datetime(df_reuters_articles['datetime']).dt.tz_localize(None) # convert Date column items to datetime.date
df_reuters_articles.set_index('Date', inplace=True) # set Date as row index
df_reuters_articles.drop('datetime', axis=1, inplace=True)
df_reuters_articles.sort_index(inplace=True)



print(df_bitcoin.info())
print(df_kyodo_articles.info())
print(df_reuters_articles.info())



# merge three data sets

# compile the list of dataframes to merge
data_frames = [df_bitcoin, df_kyodo_articles, df_reuters_articles]


df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Date'],
                                                how='outer'), data_frames)

df_merged.to_csv('../data/output/merged/merged.csv',  na_rep='.')


df_bitcoin_keywords = df_merged.query('keywords.str.contains("abc")', engine='python')
print(df_bitcoin_keywords)


# %% Clean Data
