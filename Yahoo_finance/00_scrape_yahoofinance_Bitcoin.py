# %%
import pandas as pd
import yfinance as yf
import os


ticker = yf.Ticker('BTC-USD')
df_btc_usd = ticker.history(period="5y", interval="1d")
print(df_btc_usd.head())

file = 'Yahoo_BTC_src.csv'
current_dir = os.path.abspath(os.getcwd())
output_dir = os.path.join(current_dir, '../data/input/source')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
try:
    df_btc_usd.to_csv(os.path.join(output_dir, file))
except:
    print(f'could not store data')



