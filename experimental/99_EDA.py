import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os


# %%
# get current working directory
current_dir = os.path.abspath(os.getcwd())
input_dir = os.path.join(current_dir, '../data/input')

# Loading of dataset. Load empty dataset if File not found
file ='btc_5y1d.csv'
try:
    df = pd.read_csv(os.path.join(input_dir, file))
except FileNotFoundError:
    print(f'file {file} not found')
    df = pd.DataFrame()

print(df)


#plt.plot(df.loc[:, 'Close'])
#plt.show()
print(df.loc[:, 'Close'])
df_log = np.log(df.loc[:, 'Close'])
print(df_log)
print(sm.tsa.stattools.adfuller(np.diff(df_log)))
plt.plot(np.diff(df_log))
plt.show()
sm.graphics.tsa.plot_acf(np.diff(df_log))
plt.show()
