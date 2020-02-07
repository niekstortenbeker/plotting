import prepare_data
import plot_methods as m
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np


# start from base excel?
excel = True


base = Path(__file__).resolve().parents[1]  # resolve obtains absolute path and resolves symlinks


def main():
    if excel:
        df = prepare_data.prepare_data_df()
        df_regression = pd.read_csv(base / 'data'/ 'regression.csv')
    else:
        df = pd.read_csv(base / 'data' / 'data.csv')
        df_regression = pd.read_csv(base / 'data' / 'regression.csv')
    plotting(df, df_regression)


def plotting(df, df_regression):
        plot_and_export('culture_1', df, df_regression)
        plot_and_export('culture_2', df, df_regression)
        plot_and_export('control', df, df_regression, regression=False)


def plot_and_export(culture, df, df_regression, regression=True):
    df_culture = df[df.culture == culture]
    df_regression_culture = df_regression[df_regression.culture == culture]
    fig = plot_substrates(df_culture, df_regression_culture, regression)
    m.export_plot(fig, base / 'results' / f'{culture}.png')  # or .eps, pdf etc.


def plot_substrates(df, df_regression, regression=True):
    day = df.day.values
    substrate = df.substrate_umol.values
    productA = df.productA_umol.values
    productB = df.productB_umol.values
    productC = df.productC_umol.values

    fig, axs = plt.subplots(2, sharex='all', figsize=(6, 4))
    axs[0].plot(day, substrate,
                marker='o',
                c=m.black,
                linestyle='None',
                label='substrate',
                clip_on=True)

    axs[1].plot(day, productA,
                marker='s',
                c=m.red,
                linestyle='None',
                label='product A',
                clip_on=True)
    axs[1].plot(day, productB,
                marker='D',
                c=m.purple,
                linestyle='None',
                label='product B',
                )
    axs[1].plot(day, productC,
                marker='D',
                c=m.blue,
                linestyle='None',
                label='product C')

    if regression:
        axs = trendlines(axs, df_regression)

    axs[0] = format_yax(axs[0], lim=50)
    axs[1] = format_xax(axs[1])
    axs[1] = format_yax(axs[1], lim=100)

    axs[0].legend()
    axs[1].legend()
    return fig


def trendlines(axs, df_regression):
    productB = df_regression[df_regression.y_name == 'productB_umol']
    axs[1] = add_trendlines(axs[1], productB)
    productA = df_regression[df_regression.y_name == 'productA_umol']
    axs[1] = add_trendlines(axs[1], productA)
    df_substrate = df_regression[df_regression.y_name == 'substrate_umol']
    axs[0] = add_trendlines(axs[0], df_substrate)
    return axs


def add_trendlines(ax, df):
    for index, row in df.iterrows():
        slope = row.slope
        intercept = row.intercept
        x = np.fromstring(row.x_values, dtype=np.float, sep=' ')
        ax = plot_trendline(ax, x, slope, intercept)
    return ax


def format_xax(ax, lim=None):
    ax.set_xlabel('day')
    ax.tick_params('x')
    if lim:
        ax.set_xlim(0, lim)
    else:
        ax.set_xlim(0)
    return ax


def format_yax(ax, lim=None):
    ax.set_ylabel('compound (umol)', color=m.black)
    ax.tick_params('y', colors=m.black)
    if lim:
        ax.set_ylim(0, lim)
    else:
        ax.set_ylim(0)
    return ax


def plot_trendline(ax, x, slope, intercept):
    ax.plot(x, x * slope + intercept,
            c=m.black,
            linewidth=0.5)
    return ax


if __name__ == '__main__':
    main()
