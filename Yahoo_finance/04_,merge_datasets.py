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
# reuters data is in normalized form, we wanna knwo the keywords, so the articels-keywords realtions table as well as
# he keywords table a also loaded
df_reuters_article_keyword = pd.read_csv("../data/output/normalized_stage/article_keyword.csv", index_col=0)
df_reuters_keyword = pd.read_csv("../data/output/normalized_stage/keywords.csv", index_col=0)

# Kyodo news
# Normalize Date format so only Date without time is kept. Then create newIndex 'Date' and drop old 'datetime' column
df_kyodo_articles["Date"] = pd.to_datetime(df_kyodo_articles['datetime']).dt.normalize()
df_kyodo_articles.set_index('Date', inplace=True) # set Date as row index
df_kyodo_articles.drop('datetime', axis=1, inplace=True)
df_kyodo_articles.sort_index(inplace=True)


# Reuters
df_reuters = df_reuters_articles.merge(df_reuters_article_keyword, how='left', left_on='id', right_on='article_id')
df_reuters = df_reuters.merge(df_reuters_keyword, how='left', left_on='keyword_id', right_on='id')
# Normalize Date format so only Date without time is kept. Then create newIndex 'Date' and drop old 'datetime' column
df_reuters_articles["Date"] = pd.to_datetime(df_reuters_articles['datetime']).dt.tz_localize(None)
df_reuters_articles["Date"] = df_reuters_articles["Date"].dt.normalize()
df_reuters_articles.set_index('Date', inplace=True) # set Date as row index
df_reuters_articles.drop('datetime', axis=1, inplace=True)
df_reuters_articles.sort_index(inplace=True)

# info on datasets
print(df_bitcoin.info())
print(df_kyodo_articles.info())
print(df_reuters_articles.info())


# merge three data sets
# compile the list of dataframes to merge
data_frames = [df_bitcoin, df_kyodo_articles, df_reuters_articles]


df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Date'],
                                                how='inner'), data_frames)

file = 'merged.csv'
outdir = '../data/output/merged'
if not os.path.exists(outdir):
    os.makedirs(outdir)
try:
    df_merged.to_csv(os.path.join(outdir, file), na_rep='.')
except:
    print(f'could not store data')
