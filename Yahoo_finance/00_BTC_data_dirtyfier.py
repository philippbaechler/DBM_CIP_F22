# #
# This script willdirty the previously clean data scraped from Yahooo Finance.
# These dirty data is then stored in a single table: data/output/Yahoo_BTC_src_dirty.csv
#
# The following Errors are inserted:
# - duplicated entries
# - duplicated date on different entry
# - outliers in specified column
# - missing values in specified columns
# - missing values over the whole dataset
#
# All the errors are inserted randomly. For debug purposes, every function has an argument <rndstate> to provide
# a seed value to the rng. This ensures consistent results. If not needed, one can pass None to <rndstate> to
# have random behaviour
# #


# %%
from builtins import bytes

import pandas as pd
import numpy as np
import os


def generate_outlier(data, nsigma: int, noutlier, rndstate=None):
    """
    Generate <noutlier> outliers on <data>, based on provided statistics.

    :param data: Dataframe of outliers-to-be
    :param nsigma: magnitude of distance of the generated outliers to the original  value
    :param noutlier: size of data, how many outliers to generate
    :param rndstate: random state for rng, default: None
    :return: Dataframe with randomly inserted Nan values
    """
    # generate rng with seed rndstate for reproducibility.
    rng = np.random.default_rng(seed=rndstate)
    # define upper and lower bound outliers. outliers are at least nsigma times away from the actual original entry
    upper_errors = rng.uniform(low=nsigma, high=nsigma+1, size=noutlier)
    lower_errors = rng.uniform(low=1/(nsigma+1), high=1/nsigma, size=noutlier)

    # easier to generate double amount of outliers and then only use half of it in case of odd amount of outliers
    # (spare rounding and eventual check if rounding down would create 1 missing element
    # in an odd length outlier dataset)
    outliers = np.concatenate((upper_errors, lower_errors))
    rng.shuffle(outliers)

    # now scale outlier dataset accordingly (scalar multiplication)
    data = data * (outliers[:noutlier])
    return data


def df_random_row_index(dataframe, n, rndstate=None):
    """
    Return indexes of random sample of column col of dataframe.

    :param col: str column(s) to insert Nan values
    :param dataframe: Dataframe to dirty
    :param rndstate: random state for rng, default: None
    :return: Index: series of indexes of random sample
    """
    # get row index for randomly sampled rows
    df_idx_random = dataframe.sample(frac=n, random_state=rndstate).index
    return df_idx_random


# %%
def df_insert_nan(dataframe, col: str, rndstate=None):
    """
    Add Nan values to specified dataframe column col.

    :param dataframe: Dataframe to dirty
    :param col: str column(s) to insert Nan values
    :param rndstate: random state for rng, default: None
    :return: Dataframe with randomly inserted Nan value in column col
    """

    dataframe.loc[
        df_random_row_index(dataframe, n=0.01, rndstate=rndstate), col
    ] = np.NAN
    return dataframe


def df_insert_outlier(dataframe, col: str, rndstate=None):
    """
    Add Outliers to specified numeric column col.

    :param col: str column(s) to insert Nan values
    :param dataframe: Dataframe to dirty
    :param rndstate: random state for rng, default: None
    :return: Dataframe with randomly inserted Nan values
    """

    # sample outlier dataset
    index = df_random_row_index(dataframe, n=0.01, rndstate=rndstate)
    df_outlier = dataframe.loc[index, col]

    # if already duplicated rows / values get sampled, the index gets duplicated too. so df_outlier will be noutlier+1
    # in size. That's why duplicates have to be filtered out for Outlier Generation
    df_outlier = df_outlier[~df_outlier.duplicated(keep='first')]

    # generate outliers and insert into dataset
    dataframe.loc[
        index, col
    ] = generate_outlier(data=df_outlier, nsigma=3, noutlier=len(index), rndstate=rndstate)

    return dataframe


def df_drop_rows(dataframe, query: str, rndstate=None):
    """
        Drop random rows of dataframe.

        :param col: str column(s) to insert Nan values
        :param dataframe: Dataframe to dirty
        :param rndstate: random state for rng, default: None
        :return: Dataframe with randomly dropped rows
        """

    dataframe = dataframe.drop(dataframe.query(query).sample(frac=0.01, random_state=rndstate).index)
    return dataframe


def df_insert_missing_data(dataframe, rndstate=None):
    """
    Insert missing value to random amount of rows in random columns.

    :param dataframe: Dataframe to insert Missing values
    :return: Dataframe with randomly inserted Nan values
    """
    rng = np.random.default_rng(seed=rndstate)
    for i in rng.integers(low=0, high=dataframe.index.size,
                          size=rng.integers(low=0, high=int(dataframe.index.size / 30))):
        dataframe.iloc[i, rng.integers(low=0, high=7)] = np.nan
    return dataframe


def df_duplicate_date(dataframe, rndstate=None):
    """
        Duplicate 'Date' entries in dataframe, but do not change rest of row.
        Should simulate an entry error where for two entries the same date was inserted

        :param dataframe: Dataframe to change
        :param rndstate: random state for rng, default: None
        :return: Dataframe with randomly duplicated Date entries
        """
    df_date = dataframe.sample(frac=0.01, random_state=rndstate)
    dataframe.iloc[df_date['Date'].index, 1] = dataframe.iloc[df_date['Date'].index-1, 1]
    return dataframe


def df_duplicate_rows(dataframe, rndstate=None):
    """
        Add random duplicated rows to dataframe

        :param dataframe: Dataframe to duplicate rows
        :param rndstate: random state for rng, default: None
        :return: Dataframe with randomly inserted Nan values
        """
    df_dupl = dataframe.sample(frac=0.01, random_state=rndstate)
    dataframe = pd.concat([dataframe, df_dupl], axis='index')
    dataframe['Date'] = pd.to_datetime(dataframe['Date'])
    dataframe.sort_values(by=['Date'], inplace=True)
    return dataframe


# %%
# Preparation
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


# seed variable for rngs. set to generate reproducible output
randomstate = None


# %% add impurities
# The scrapped ata form Yahoo Finance is very clean, In fact, there is not a single defect in it.
# Thus, we have to introduce some plausible bot not too systematic errors.

# First error is to duplicate rows, essentially creating duplicate entries to the dataset
df = df_duplicate_rows(df, randomstate)

# Second is to only duplicate the entry in the column 'Date', as if to entries would accidentally share the same index
df = df_duplicate_date(df, randomstate)

# One common error which is difficult to clean (and also generate) are outliers. Here outliers are inserted in the
# 'High' column. Basically all numeric columns are permitted, except the 'Date' columns
df = df_insert_outlier(df, col='High', rndstate=randomstate)

# To simulate missing values it's possible to insert random Nan in selected column(s)
df = df_insert_nan(df, col='Close', rndstate=randomstate)

# It's also possible to insert missing values randomly over all columns
df = df_insert_missing_data(df, randomstate)

# At las, delete randomly selected rows to mimic missing entries. It's possible to specify a query condition  to narrow
# down the possible candidates to drop. Here we opted for entries where the daily fluctuation was higher than 666$
df = df_drop_rows(df, query='(High - Low) > 666', rndstate=randomstate)


# %% save dirty dataset
# The now prepared dirty dataset is saved.
file = 'Yahoo_BTC_src_dirty.csv'
output_dir = os.path.join(current_dir, '../data/output/dirty')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
try:
    df.to_csv(os.path.join(output_dir, file), index=False)
except:
    print(f'could not store data')
