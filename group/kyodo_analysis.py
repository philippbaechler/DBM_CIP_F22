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
df_kyodo = df_kyodo.rename(columns={"paragraph": "text"})
df_kyodo.sort_values(by="datetime", inplace=True)
df_kyodo.reset_index(inplace=True, drop=True)
df_kyodo["year_month"] = [datetime(year=d.year, month=d.month, day=1) for d in df_kyodo["datetime"]]
df_kyodo.head(3)


# %%
number_of_articles_per_month = df_kyodo.groupby(by=[df_kyodo["year_month"]])["title"].count().to_frame().reset_index()
number_of_articles_per_month.rename(columns={"title": "number_of_articles"}, inplace=True)
number_of_articles_per_month.head()

# %%
plt.figure(figsize=FIG_DIM)
plt.plot(number_of_articles_per_month["year_month"], number_of_articles_per_month["number_of_articles"])
plt.ylabel("Number of Articles per Month")
plt.savefig("kyodoNumberArticlesTotal.pdf")


# %%
df_kishida_occurences = get_occurences_per_month(df_kyodo, "Kishida")
df_kishida_occurences.head()

# %%
plt.figure(figsize=FIG_DIM)
plt.plot(df_kishida_occurences["year_month"], df_kishida_occurences["occurences"])
plt.ylabel("Number of Articles mentioning \"Kishida\"")
plt.savefig("numberArticlesKishida.pdf")


# %%
df_edano_occurences = get_occurences_per_month(df_kyodo, "Edano")
df_edano_occurences.head()

# %%
plt.figure(figsize=FIG_DIM)
plt.plot(df_edano_occurences["year_month"], df_edano_occurences["occurences"])
plt.ylabel("Number of Articles mentioning \"Edano\"")
plt.savefig("numberArticlesEdano.pdf")

# %%
plt.figure(figsize=FIG_DIM)
plt.plot(df_kishida_occurences["year_month"], df_kishida_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])
plt.plot(df_edano_occurences["year_month"], df_edano_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])


# %%
plt.figure(figsize=FIG_DIM)

df_occurences = get_occurences_per_month(df_kyodo, "Kishida")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

df_occurences = get_occurences_per_month(df_kyodo, "Edano")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

df_occurences = get_occurences_per_month(df_kyodo, "Fumio")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

df_occurences = get_occurences_per_month(df_kyodo, "Yukio")
plt.plot(df_occurences["year_month"], df_occurences["occurences"]/number_of_articles_per_month["number_of_articles"])

plt.legend(["Kishida", "Edano", "Fumio", "Yukio"])
plt.ylabel("Percentage of Articles")
plt.savefig("KishidaEdanoVsFumioYukio.pdf")
# %%
# %%
