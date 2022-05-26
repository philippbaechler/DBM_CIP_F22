
# %%
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
from analysis_helper import *

# %%
FIG_DIM = (12,4)

# %%
df_kyodo = pd.read_csv("../data/output/kyodo_src.csv", \
                 converters={"channels": convert_string_to_list, \
                             "keywords": convert_string_to_list, \
                             "author": convert_string_to_list})
df_kyodo["datetime"] = pd.to_datetime(df_kyodo["datetime"])
df_kyodo["paragraph"] = df_kyodo["paragraph"].str.replace("[", "").str.replace("]", "")
df_kyodo = df_kyodo.rename(columns={"paragraph": "text", "datetime": "article_date_time", "author": "authors"})
df_kyodo["publisher"] = "Kyodo News"
df_kyodo.sort_values(by="article_date_time", inplace=True)
df_kyodo.reset_index(inplace=True, drop=True)
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
df_reuters = df_reuters.rename(columns={"key_words": "keywords", "content_channel": "channels"})
df_reuters["authors"] = df_reuters["main_author"] + df_reuters["reporters"] + df_reuters["writers"] + df_reuters["editors"]
df_reuters["publisher"] = "Thomson and Reuters"
df_reuters.drop(columns=(["main_author", "reporters", "writers", "editors"]), inplace=True)
df_reuters.sort_values(by="article_date_time", inplace=True)
df_reuters.reset_index(inplace=True, drop=True)
df_reuters.head(3)


# %%
df_combined = df_kyodo.append(df_reuters)
df_combined["year_month"] = [datetime(year=d.year, month=d.month, day=1) for d in df_combined["article_date_time"]]
df_combined.head()


# %%
number_of_articles_per_month = df_combined.groupby(by=[df_combined["year_month"]])["title"].count().to_frame().reset_index()
number_of_articles_per_month.rename(columns={"title": "number_of_articles"}, inplace=True)
number_of_articles_per_month.head()


# %%
plt.figure(figsize=FIG_DIM)

df_occurences = get_occurences_per_month(df_combined, "Putin")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])
df_occurences = get_occurences_per_month(df_combined, "war")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])
df_occurences = get_occurences_per_month(df_combined, "climate")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])
df_occurences = get_occurences_per_month(df_combined, "virus")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])
plt.ylabel("Percentage of Articles")
plt.legend(["Putin", "war", "climate", "virus"])
plt.savefig("PutinWarClimateVirus.pdf")


# %%
plt.figure(figsize=FIG_DIM)
df_occurences = get_occurences_per_month(df_combined, "bitcoin")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])
df_occurences = get_occurences_per_month(df_combined, "ether")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])
df_occurences = get_occurences_per_month(df_combined, "crypto")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])
plt.ylabel("Percentage of Articles")
plt.legend(["bitcoin", "ether", "crypto"])
plt.xlim((datetime(2020, 5, 1), datetime(2022, 5, 1)))
plt.savefig("BitcoinEtherCrypto.pdf")


# %%
plt.figure(figsize=FIG_DIM)

df_occurences = get_occurences_per_month(df_combined, "Bitcoin")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

df_occurences = get_occurences_per_month(df_combined, "Tesla")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

df_occurences = get_occurences_per_month(df_combined, "Twitter")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

df_occurences = get_occurences_per_month(df_combined, "Google")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

df_occurences = get_occurences_per_month(df_combined, "Facebook")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

df_occurences = get_occurences_per_month(df_combined, "Microsoft")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

df_occurences = get_occurences_per_month(df_combined, "Apple")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])


plt.legend(["Bitcoin", "Tesla", "Twitter", "Google", "Facebook", "Microsoft", "Apple"])
plt.ylabel("Percentage of Articles")
plt.savefig("techCompanies.pdf")
# %%
