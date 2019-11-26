import pandas as pd
import data_methods as m
import regression
from pathlib import Path

pd.set_option('display.width', 190)
pd.set_option('display.max_columns', None)

base = Path(__file__).resolve().parents[1]  # resolve obtains absolute path and resolves symlinks
data = base / 'data'


def prepare_data_df():
    startdate = '2018-12-14'
    df = m.df_from_base_excel(data / 'data.xlsx', data / 'data.csv')
    df = m.get_day_delta(df, startdate)
    df = calc_amount_productB_and_C(df)
    df = calc_amount_gasses(df)
    m.export_dataframe(df, data / 'data.csv')
    regression.prepare_regression_csv(df)
    return df


def calc_amount_productB_and_C(df):
    df['productB_umol'] = df['productB_uM'] * df['culture_volume_ml'] / 1000
    df['productC_umol'] = df['productC_uM'] * df['culture_volume_ml'] / 1000
    return df


def calc_amount_gasses(df):
    df['substrate_umol'] = df.apply(calc_amount_gas, args=(1.9E-3, 'substrate_ppm'), axis=1)
    df['productA_umol'] = df.apply(calc_amount_gas, args=(24E-3, 'productA_ppm'), axis=1)
    return df


def calc_amount_gas(row, henry_constant, gas_ppm):
    """calculate total amount of a specific gas in umol, originating from the headspace and liquid phase"""
    # amount of all gasses in headspace
    amount_headspace = m.volume_to_mol(temperature_C=20,
                                       overpressure_bar=row['overpressure_bar'],
                                       volume_ml=row['headspace_volume_ml'])  # in mol
    # amount of specific gas in headspace
    amount_headspace = amount_headspace / 1E6 * row[gas_ppm]  # in mol
    amount_headspace = amount_headspace * 1E6  # in umol
    # amount of specific gas in liquid phase
    concentration_dissolved = m.henry(ppm=row[gas_ppm],
                                      overpressure_bar=row['overpressure_bar'],
                                      henry_constant=henry_constant)  # in mol * l-1
    amount_liquid = row['culture_volume_ml'] * 1E-3 * concentration_dissolved  # in mol
    amount_liquid = amount_liquid * 1E6  # in umol
    return amount_headspace + amount_liquid


if __name__ == '__main__':
    prepare_data_df()

