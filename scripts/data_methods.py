import pandas as pd
import csv
import openpyxl
import arrow


def df_from_base_excel(fin, fout):
    """first convert excel to csv, then pandas read_csv, """
    excel_to_csv(fin, fout)
    df = pd.read_csv(fout)
    return df


def excel_to_csv(fin, fout):
    wb = openpyxl.load_workbook(fin)
    sh = wb.active
    with open(fout, 'w', newline='') as f:
        c = csv.writer(f)
        for r in sh.rows:
            c.writerow([cell.value for cell in r])


def export_dataframe(df, fout):
    df.to_csv(fout, index=False, na_rep='NA')
    print('exported a csv to:', fout)


def get_day_delta(df, startdate):
    """add a column to dataframe that calculates the delta in days between startdate and the column date"""
    df['day'] = df.date.apply(date_to_day, startdate=startdate)
    return df


def date_to_day(date, startdate):
    """for any given date, calculate the delta in days from startdate"""
    day1 = arrow.get(startdate)
    date = date.strip()
    if len(date) == 8:
        try:
            date = arrow.get(str(date), 'YYYYMMDD')
            day = date - day1
            day = int(day.days)
            return day
        except arrow.parser.ParserError as error:
            print(f'a date ({date}) could not be converted, full info:')
            print(error)
            return date
    else:
        try:
            date = arrow.get(str(date))
            day = date - day1
            day = int(day.days)
            return day
        except arrow.parser.ParserError as error:
            print(f'a date ({date}) could not be converted, full info:')
            print(error)
            return date


def volume_to_mol(temperature_C, overpressure_bar, volume_ml):
    """calculate molar amount of a gas using ideal gas law"""
    temperature = temperature_C + 273.15  # celcius to Kelvin
    pressure = overpressure_bar * 0.9869233 + 1  # bar to atm, + atmospheric pressure
    volume = volume_ml / 1000  # ml to l
    R = 0.082057 # L*atm*K-1*mol-1
    Vm = R * temperature / pressure # ideal gas law
    n = volume / Vm
    return n


def henry(ppm, overpressure_bar, henry_constant):
    """Use Henry's law to calculate dissolved concentration of a specific gas in solution in mol*l-1. 
    henry_constant should be in M * atm-1"""
    pressure = overpressure_bar * 0.9869233 + 1  # bar to atm, + atmospheric pressure
    partial_pressure = pressure / 1E6 * ppm
    concentration_dissolved = partial_pressure * henry_constant  # in mol * l-1
    return concentration_dissolved