# %%
import pandas as pd
import sqlalchemy
import timeit


# %% load data frame
keywords = pd.read_csv("data/output/keywords.csv", index_col=0)
keywords.head()


# %% constring = "mssql+pyodbc://USERNAME:PASSWORD@DATABASESERVER_IP/DATABASENAME?driver=SQL+Server+Native+Client+11.0"
usr = "root"
passwd = ""
constring = f'mysql+pymysql://{usr}:{passwd}@localhost/'
dbEngine = sqlalchemy.create_engine(constring, connect_args={'connect_timeout': 10}, echo=False)
dbEngine.execute("USE mydb")


# %%
def test_mysql_connection():
    try:
        with dbEngine.connect() as con:
            con.execute("SELECT 1")
        print('engine is valid')
    except Exception as e:
        print(f'Engine invalid: {str(e)}')


def get_content_of_keywords_t():
    dbEngine.execute("USE mydb")
    output = dbEngine.execute("SELECT * FROM keywords_t").fetchall()
    output


def delete_content_of_keywords_t():
    dbEngine.execute("DELETE FROM keywords_t;")


# 1. version ".to_sql()"
def to_sql_version_1():
    keywords.to_sql(name="keywords_t", con=dbEngine, schema="mydb", if_exists="append", index=False)


# 2. version "chunking"
def to_sql_version_2():
    keywords.to_sql(name="keywords_t", con=dbEngine, schema="mydb", \
        if_exists="append", index=False, chunksize=1000)


# 3. version  "multi-insert"
def to_sql_version_3():
    keywords.to_sql(name="keywords_t", con=dbEngine, schema="mydb", \
        if_exists="append", index=False, chunksize=1000, method='multi')



#%%
print(timeit.timeit(lambda: to_sql_version_1(), number=1))
delete_content_of_keywords_t()

#%%
print(timeit.timeit(lambda: to_sql_version_2(), number=1))
delete_content_of_keywords_t()

#%%
print(timeit.timeit(lambda: to_sql_version_3(), number=1))
delete_content_of_keywords_t()


# %%
