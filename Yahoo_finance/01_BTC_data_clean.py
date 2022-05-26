# #
# This script will clean the previously 'dirtified' data scraped from Yahooo Finance.
# These cleaned data is then stored in a single table: data/output/clean/ Yahoo_BTC_src_stage.csv
#
# The following Errors are considered:
# - duplicated entries
# - missing Date entry
# - missing rows
# - outlier detection and correction
#
# #

# %%
import numpy as np
import pandas as pd
import os

# %% set pandas  options
pd.set_option('display.max_columns', 0)  # Display any number of columns
pd.set_option('display.max_rows', 0)  # Display any number of rows
pd.set_option('expand_frame_repr', False)


def clean_duplicates(df):
    """
        search for duplicated entries and delete them.
        :param: df entry dataframe
        :return: Dataframe with randomly inserted Nan values
        """
    # check for duplicates and keep first entry, delete rest
    df = df[~df.duplicated(keep='first')]

    # check if there are any left (should be 0)
    print(len(df[df.duplicated()]))
    return df


def clean_missing_date(df):
    """
    clean missing 'Date' entries. If Date is missing, later the Dataset cannot be joined with the othe rdatasets.
    Therefore, Date information has to be inserted if missing
    :param: df entry dataframe
    :return: Dataframe with randomly inserted Nan values
    """

    # find first datetime entry in dataframe
    t0 = df['Date'].min()

    # check for which entries are missing by creating boolean vector
    df_date_available = df['Date'].notnull()

    # convert datetime to integers that are smaller than the full 64bit range, so pandas interpolation can work with
    # them. Note: use boolean df_date_available to avoid subtracting on Nan's --> error
    df.loc[df_date_available, 't_int'] = (df.loc[df_date_available, 'Date'] - t0).dt.total_seconds()

    # interpolate the missing Dates
    df['Date'] = t0 + pd.to_timedelta(df.t_int.interpolate(), unit='s')

    # 'Date' is no longer only Date due to numerical errors while interpolating. Normalize to get hh:mm:ss = 00:00:00
    df['Date'] = pd.to_datetime(df['Date']).dt.normalize()
    # drop not needed columns
    df.drop('t_int', axis=1, inplace=True)

    return df


def clean_missing_entries(df):
    """
    search for complete missing rows / entries.
    Adapt DateTimeIndex range to create new entries for missing ones and interpolate based on previous/next values

    :param: df entry dataframe
    :return: Dataframe with randomly inserted Nan values
    """
    # generate continious date range (DateTimeIndex) from earliest entry to most recent entry
    date_range = pd.date_range(
        start=f'{df.Date.min()}', end=f'{df.Date.max()}', freq='D')

    # set 'Date' as index and resize to date_range created index. afterwards reset index, so 'Date' again can be a value
    # rename is need because Pandas doesn't know previous indexes name. With expanding the index, before missing rows
    # are created, as index is now truly continuous RangeIndex.
    df = df.set_index('Date').reindex(index=date_range).reset_index().rename(columns={'index': 'Date'})

    # newly created rows do have a Date entry, but rest is NaN. Interpolate to fill in values. Daily Fluctuations
    # should in the grand scale be reasonably be within previous and next day.
    df.loc[:, df.columns != 'Date'] = df.loc[:, df.columns != 'Date'].interpolate(method='linear', direction='forward')

    return df


def clean_outliers(df):
    """
    Search for outliers and replace them with averaged values.
    For outlier detection package 'ADTK' is used, see here: https://arundo-adtk.readthedocs-hosted.com/en/stable/#
    Detection Metric is IQR (inter quartile range)

    :param: df entry dataframe
    :return: df outlier cleaned Dataframe
    """

    # Laad package
    from adtk.data import validate_series
    from adtk.detector import InterQuartileRangeAD
    from adtk.visualization import plot

    # set Date as Index
    df.set_index('Date', inplace=True)

    # check if Dataset is compatile with the package
    df = validate_series(df)

    # No errors raised, so look at data. please close
    plot(df)

    # Based on Plot: seems like outliers are present in column 'High' and 'Volume'.
    # Use InterQuartileRange detection method to find outliers
    iqr_ad = InterQuartileRangeAD(c=1.7)
    anomalies = iqr_ad.fit_detect(df)

    # check detected anomalies with plot
    # plot(data, anomaly=anomalies, anomaly_color="orange", anomaly_tag="marker")

    # Set outliers to Nan
    df[((anomalies['High'] == True) | (anomalies['Volume'] == True))] = np.nan
    df[anomalies == True] = np.nan

    # Interpolate outliers, as we need every timestamp for later connection in the Database
    df = df.interpolate()

    return df


# %%
# Preparation

# get current working directory
current_dir = os.path.abspath(os.getcwd())
input_dir = os.path.join(current_dir, '../data/output/dirty')

# Loading of dataset. Load empty dataset if File not found
file = 'Yahoo_BTC_src_dirty.csv'
try:
    df = pd.read_csv(os.path.join(input_dir, file),
                     parse_dates=['Date']
                     )
except FileNotFoundError:
    print(f'file {file} not found')
    df = pd.DataFrame()

# %% Clean Data

# %%
# Check for data types
print(df.dtypes)
# Stock Splits is int64, whereas others are float64. Convert to float, which also makes more sense for a ratio information.
df['Stock Splits'] = df['Stock Splits'].astype(float)
print(df.dtypes)

# View dataset
print(df.head())

# as we see that the last 2 columns report only 0, we check the whole dataframe and remove the ones that have only
# 0 or NAs
f = df.replace([0, 'NA'], np.nan).apply(lambda x: any(~x.isnull()))
df = df.loc[:, f]


# %%
# Check for duplicates.
print(len(df[df.duplicated()]))

# As there are duplicates, clean/drop them
df = clean_duplicates(df)

# %%
# Check for missing date entries
print(len(df[df["Date"].isnull()]))

# Date entry is most important for later merging with other Datasets, so must be continous.
df = clean_missing_date(df)

# no Missing Date entries anymore
print(len(df[df["Date"].isnull()]))

# %%
# Check for missing entries

# as we know we had missing Date values, it could be entire entries are missing.
df = clean_missing_entries(df)

# %%
# Outlier Detection
df = clean_outliers(df)

# %% save cleaned dataset
# The now cleaned dataset is saved.
file = 'Yahoo_BTC_src_stage.csv'
outdir = os.path.join(current_dir, '../data/output/clean')
if not os.path.exists(outdir):
    os.makedirs(outdir)
try:
    df.to_csv(os.path.join(outdir, file))
except:
    print(f'could not store data')
