# %%
import pandas as pd
import yfinance as yf


ticker = yf.Ticker('BTC-USD')
df_btc_usd = ticker.history(period="5y", interval="1d")

with open('../btc_5y1d.csv', 'w') as file:
    file.write(df_btc_usd.to_csv())



