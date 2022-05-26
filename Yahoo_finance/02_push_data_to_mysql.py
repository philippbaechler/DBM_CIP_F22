# %%
import pandas as pd
import sqlalchemy


# %% load data
df_Bitcoin = pd.read_csv("../data/output/clean/Yahoo_BTC_src_stage.csv", index_col=0)


# %% connect to mysql data base
usr = "root"
passwd = "oEK*#3NHDfizWP"
connector_string = f'mysql+pymysql://{usr}:{passwd}@localhost/'
dbEngine = sqlalchemy.create_engine(connector_string, connect_args={'connect_timeout': 10}, echo=False)
dbEngine.execute("USE CIP")


# %%
def push_df_to_mysql_table(data_frame, table_name):
    data_frame.to_sql(name=table_name, con=dbEngine, schema="cip", \
        if_exists="replace", index=False, chunksize=1000, method='multi')


# %%
push_df_to_mysql_table(df_Bitcoin, "bitcoin_t")





# %%
