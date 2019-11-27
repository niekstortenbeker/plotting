from pathlib import Path
import numpy as np
from scipy import stats
import csv
import pandas as pd

pd.set_option('display.width', 190)
pd.set_option('display.max_columns', None)

base = Path(__file__).resolve().parents[1]  # resolve obtains absolute path and resolves symlinks
data = base / 'data'


def prepare_regression_csv(df):
    """for products make trendlines for the different cultures, for substrate make different trendlines for different
    cultures and fed number"""
    df = remove_outliers(df)

    with open(data / 'regression.csv', 'w') as fout:
        print(f'exported a csv to: {fout.name}')
        writer = csv.writer(fout)
        writer.writerow(['culture', 'x_name', 'y_name', 'slope', 'intercept', 'r_squared', 'x_values', 'y_values'])

        cultures = df.culture.unique()
        for culture in cultures:
            # groupby would be a better solution here
            df_trendline = df[df.culture == culture]
            write_regression(culture, 'productA_umol', df_trendline, writer)
            write_regression(culture, 'productB_umol', df_trendline, writer)

            feeding = df_trendline.fed.unique()
            for fed in feeding:
                df_trendline_substrate = df_trendline[df_trendline.fed == fed]
                write_regression(culture, 'substrate_umol', df_trendline_substrate, writer)
    return df


def write_regression(culture, substrate, df, writer):
    day_trendline, substrate_trendline = data_for_trendline(df, 'day', substrate, drop_zero=True)
    if len(day_trendline) < 3:  # you don't want a trendline if you have less than 3 points
        return
    try:
        slope, intercept, r_squared = linear_regression(day_trendline, substrate_trendline)
        writer.writerow(
            [culture, 'day', substrate, slope, intercept, r_squared, np2str(day_trendline), np2str(substrate_trendline)])
        return
    except ValueError:
        return


def remove_outliers(df):
    # on these two days productB data is off
    df.loc[df.day == 91, 'productB_umol'] = np.NaN
    df.loc[df.day == 104, 'productB_umol'] = np.NaN
    return df


def np2str(array):
    return np.array2string(array)[1:-1]


def linear_regression(x, y):
    mask = ~np.isnan(x) & ~np.isnan(y)  # create mask to remove NANs
    slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask], y[mask])
    return slope, intercept, r_value ** 2


def data_for_trendline(df, x, y, drop_zero = False, outliers = None):
    """outliers should be list of two items: first column name and then list of values to remove.
    generally, you don't want to include zero's in a trendline"""
    df = df.dropna(subset=[y])
    if drop_zero:
        df = df[df[y] != 0]
    if outliers:
        df = df[~df[outliers[0]].isin(outliers[1])]
    return df[x].values, df[y].values


