# %%
import pandas as pd
import numpy as np

with open('../btc_5y1d.csv', 'r') as file:
    try:
        df = pd.read_csv(file, index_col=0)
    except FileNotFoundError:
        print(f'file {file} not found')
        df = pd.DataFrame()

print(df.to_string(max_rows=10))
print(str(df))


# %%
# add impurities

def dirty_close_values(dataframe):
    print(dataframe['Close'].sample(n=int(dataframe['Close'].size*0.1)))
    dataframe['Close'].replace(to_replace=dataframe['Close'].sample(n=int(dataframe.size*0.1)), value=1)
    return dataframe

df = dirty_close_values(df)
print(df.to_string(max_rows=100))



# %%
