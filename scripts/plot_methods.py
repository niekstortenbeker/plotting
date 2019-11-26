import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

black = (0, 0, 0)
blue = (0.149, 0.365, 0.670)
orange = (0.875, 0.361, 0.141)
green = (0.20, 0.592, 0.282)
pink = (0.898, 0.071, 0.435)
brown = (0.616, 0.447, 0.165)
purple = (0.533, 0.337, 0.654)
yellow = (0.780, 0.706, 0.180)
red = (0.796, 0.125, 0.152)
grey = (0.827, 0.827, 0.827)
darkgrey = (0.745, 0.745, 0.745)


def export_plot(figure, directory, tight=False):
    print("exported an image to: ", directory)
    if tight:
        return figure.savefig(directory, dpi=600, bbox_inches='tight')
    else:
        return figure.savefig(directory, dpi=600)


def plot_legend(ax1, ax2=None, ax3=None, figsize=None):
    """plot the legend in a separate figure. axes should be an iterable, also if there is only one"""
    if not figsize:
        figsize = [1.5, 1]
    fig_legend, axi = plt.subplots(figsize=(figsize[0], figsize[1]))
    # get the handles and labels. If there are more axes, create one list with all the handles and labels
    handles, labels = ax1.get_legend_handles_labels()
    if ax2:
        handles_ax2, labels_ax2 = ax2.get_legend_handles_labels()
        handles = handles + handles_ax2
        labels = labels + labels_ax2
    if ax3:
        handles_ax3, labels_ax3 = ax3.get_legend_handles_labels()
        handles = handles + handles_ax3
        labels = labels + labels_ax3
    axi.legend(handles, labels, loc='center')
    # remove x axis
    axi.xaxis.set_visible(False)
    # remove y axes
    axi.yaxis.set_visible(False)
    # remove spines
    axi.spines['right'].set_visible(False)
    axi.spines['left'].set_visible(False)
    axi.spines['top'].set_visible(False)
    axi.spines['bottom'].set_visible(False)
    # fig_legend.tight_layout()
    return fig_legend


def linear_regression(x, y):
    mask = ~np.isnan(x) & ~np.isnan(y)  # create mask to remove NANs
    slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask], y[mask])
    return slope, intercept, r_value ** 2


def add_trendline(x, y, ax):
    slope, intercept, r_squared = linear_regression(x, y)
    print(f'slope: {slope}, intercept:{intercept}, r squared: {r_squared}')
    ax.plot(x, x * slope + intercept,
            c=black,
            linewidth=0.5)
    return ax


def data_for_trendline(df, x, y, outliers = None):
    """outliers should be list of two items: first column name and then list of values to remove"""
    df = df.dropna(subset=[y])
    if outliers:
        df = df[~df[outliers[0]].isin(outliers[1])]
    return df[x].values, df[y].values