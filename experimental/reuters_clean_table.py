# %%
import pandas as pd


# %%
def convert_string_to_list(string_input):
    return string_input.replace("'", "")\
                       .replace("[", "")\
                       .replace("]", "")\
                       .split(", ")


# %%
df = pd.read_csv("data/output/reuters_dirty.csv", index_col=0, \
                 converters={"key_words": convert_string_to_list, \
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
# Sort articles by datetime
df.sort_values(by="article_date_time", inplace=True)
df.reset_index(inplace=True, drop=True)
df.head(10)

# %%
# example keywords before 2021-04-08
df.iloc[24161]["key_words"]

# %%
# example keywords after 2021-04-09
df.iloc[24180]["key_words"]


# %%
# Restrict to articles before 
df_sub = df[df["article_date_time"] < '2021-04-08']
df_sub.head()


# %%


# %%
df.to_csv("data/output/reuters_sorted.csv")

# %%

# %%

# %%
