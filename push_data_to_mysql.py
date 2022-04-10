# %%
import pandas as pd
import sqlalchemy


# %% load data frame
df_keywords = pd.read_csv("data/output/keywords.csv", index_col=0)
df_articles = pd.read_csv("data/output/articles.csv", index_col=0)
df_describes = pd.read_csv("data/output/describes.csv", index_col=0)


# %%
usr = "root"
passwd = ""
constring = f'mysql+pymysql://{usr}:{passwd}@localhost/'
dbEngine = sqlalchemy.create_engine(constring, connect_args={'connect_timeout': 10}, echo=False)
dbEngine.execute("USE mydb")


# %%
def push_df_to_mysql_table(data_frame, table_name):
    data_frame.to_sql(name=table_name, con=dbEngine, schema="mydb", \
        if_exists="append", index=False, chunksize=1000, method='multi')


# %%
push_df_to_mysql_table(df_keywords, "keywords_t")

# %%
push_df_to_mysql_table(df_articles, "articles_t")

# %%
push_df_to_mysql_table(df_describes, "article_keyword")


# %%
