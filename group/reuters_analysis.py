# %%
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
from analysis_helper import *


# %%
FIG_DIM = (12,4)


# %%


# %%
df_reuters = pd.read_csv("../data/output/reuters_dirty.csv", index_col=0, \
                 converters={"key_words": convert_string_to_list, \
                             "main_author": convert_string_to_list, \
                             "reporters": convert_string_to_list, \
                             "writers": convert_string_to_list, \
                             "editors": convert_string_to_list})

df_reuters["article_date_time"] = pd.to_datetime(df_reuters["article_date_time"])
df_reuters = df_reuters[df_reuters["article_date_time"].notnull()]
df_reuters.sort_values(by="article_date_time", inplace=True)
df_reuters.reset_index(inplace=True, drop=True)
df_reuters["year_month"] = [datetime(year=d.year, month=d.month, day=1) for d in df_reuters["article_date_time"]]
df_reuters.head(3)


# %%
number_of_articles_per_month = df_reuters.groupby(by=[df_reuters["year_month"]])["title"].count().to_frame().reset_index()
number_of_articles_per_month.rename(columns={"title": "number_of_articles"}, inplace=True)
number_of_articles_per_month.head()

# %%
plt.figure(figsize=FIG_DIM)
plt.plot(number_of_articles_per_month["year_month"], number_of_articles_per_month["number_of_articles"])
plt.ylabel("Number of Articles per Month")
plt.savefig("numberArticlesTotal.pdf")


# %%
df_trump_occurences = get_occurences_per_month(df_reuters, "Trump")
df_trump_occurences.head()

# %%
plt.figure(figsize=FIG_DIM)
plt.plot(df_trump_occurences["year_month"], df_trump_occurences["occurences"])
plt.ylabel("Number of Articles mentioning \"Trump\"")
plt.savefig("numberArticlesTrump.pdf")


# %%
df = number_of_articles_per_month.merge(df_trump_occurences, how="left", on="year_month")
df["percent_trump"] = df["occurences"]/df["number_of_articles"]
df = df.drop(columns=["occurences"])
df.head()


# %%
plt.figure(figsize=FIG_DIM)
plt.plot(df["year_month"], df["percent_trump"])
plt.ylabel("Percentage of Articles mentioning \"Trump\"")
plt.savefig("percentageTrump.pdf")


# %%
df_biden_occurences = get_occurences_per_month(df_reuters, "Biden")
df = df.merge(df_biden_occurences, how="left", on="year_month")
df["percent_biden"] = df["occurences"]/df["number_of_articles"]
df = df.drop(columns=["occurences"])
df.head()


# %%
df_obama_occurences = get_occurences_per_month(df_reuters, "Obama")
df = df.merge(df_obama_occurences, how="left", on="year_month")
df["percent_obama"] = df["occurences"]/df["number_of_articles"]
df = df.drop(columns=["occurences"])
df.head()


# %%
plt.figure(figsize=FIG_DIM)
plt.plot(df["year_month"], df["percent_trump"])
plt.plot(df["year_month"], df["percent_biden"])
plt.plot(df["year_month"], df["percent_obama"])
plt.legend(["Trump", "Biden", "Obama"])
plt.ylabel("Percentage of Articles")
plt.savefig("trumpBidenObama.pdf")


# %%
plt.figure(figsize=FIG_DIM)

df_occurences = get_occurences_per_month(df_reuters, "Bitcoin")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

df_occurences = get_occurences_per_month(df_reuters, "Tesla")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

df_occurences = get_occurences_per_month(df_reuters, "Twitter")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

df_occurences = get_occurences_per_month(df_reuters, "Google")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

df_occurences = get_occurences_per_month(df_reuters, "Facebook")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

df_occurences = get_occurences_per_month(df_reuters, "Microsoft")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

df_occurences = get_occurences_per_month(df_reuters, "Apple")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])


plt.legend(["Bitcoin", "Tesla", "Twitter", "Google", "Facebook", "Microsoft", "Apple"])
plt.ylabel("Percentage of Articles")
plt.savefig("techCompanies.pdf")



