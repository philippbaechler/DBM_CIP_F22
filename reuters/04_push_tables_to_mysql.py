# %%
import pandas as pd
import sqlalchemy


# %% load data frame
df_article_author = pd.read_csv("data/output/normalized/article_author.csv", index_col=0)
df_article_keyword = pd.read_csv("data/output/normalized/article_keyword.csv", index_col=0)
df_articles = pd.read_csv("data/output/normalized/articles.csv", index_col=0)
df_author_role = pd.read_csv("data/output/normalized/author_role.csv", index_col=0)
df_authors = pd.read_csv("data/output/normalized/authors.csv", index_col=0)
df_keywords = pd.read_csv("data/output/normalized/keywords.csv", index_col=0)
df_roles = pd.read_csv("data/output/normalized/roles.csv", index_col=0)


# %% connect to mysql data base
usr = "root"
passwd = ""
constring = f'mysql+pymysql://{usr}:{passwd}@localhost/'
dbEngine = sqlalchemy.create_engine(constring, connect_args={'connect_timeout': 10}, echo=False)
dbEngine.execute("USE dbm_project_db")


# %%
def push_df_to_mysql_table(data_frame, table_name):
    data_frame.to_sql(name=table_name, con=dbEngine, schema="dbm_project_db", \
        if_exists="replace", index=False, chunksize=1000, method='multi')


# %%
push_df_to_mysql_table(df_article_author, "article_author_t")

# %%
push_df_to_mysql_table(df_article_keyword, "article_keyword_t")

# %%
push_df_to_mysql_table(df_articles, "articles_t")

# %%
push_df_to_mysql_table(df_author_role, "author_role_t")

# %%
push_df_to_mysql_table(df_authors, "authors_t")

# %%
push_df_to_mysql_table(df_keywords, "keywords_t")

# %%
push_df_to_mysql_table(df_roles, "roles_t")




# %%
