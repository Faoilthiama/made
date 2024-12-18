import urllib.request
from urllib.error import URLError

import pandas as pd
import sqlite3

DATASET1 = "dataset1.xls"
DATASET2 = "dataset2.xls"


def download_datasets():
    print('Downloading datasets...')
    for i in range(3):
        try:
            urllib.request.urlretrieve("https://api.worldbank.org/v2/en/indicator/SP.DYN.LE00.IN?downloadformat=excel",
                                       DATASET1)
            urllib.request.urlretrieve(
                "https://api.worldbank.org/v2/en/indicator/SH.XPD.CHEX.PP.CD?downloadformat=excel",
                DATASET2)
            with pd.ExcelFile(DATASET1) as df1, pd.ExcelFile(DATASET2) as df2:
                return df1, df2
        except URLError as e:
            if i < 2:
                print('Oops. Something went wrong with the download.')
                print(f'Retrying for the {i + 1}. time.')
            else:
                print('Aborting pipeline due to too many failed download attempts.')
                raise Exception('Download failed', e)


def clean_data(dataset):
    print(f'Cleaning data...')
    try:
        countries = dataset.parse('Metadata - Countries')

        lac_country_codes = _get_country_codes(countries)

        data_sheet = _filter_countries(dataset, lac_country_codes)

        data_sheet = _drop_irrelevant_columns(data_sheet)

        data_sheet = _drop_empty_rows(data_sheet)
        return _fill_NaN(data_sheet)
    except Exception as e:
        print('Something went wrong during data cleaning.')
        raise Exception('Data cleaning failed', e)


def _fill_NaN(data):
    year_columns = [str(year) for year in range(2000, 2022)]
    data[year_columns] = data[year_columns].apply(lambda row: row.ffill(), axis=1)
    data[year_columns] = data[year_columns].apply(lambda row: row.bfill(), axis=1)
    data[year_columns] = data[year_columns].apply(lambda row: row.interpolate(method='linear', axis=0), axis=1)
    return data


def _drop_empty_rows(data_sheet):
    columns_to_check = [str(year) for year in range(2000, 2022)]
    data_sheet = data_sheet.dropna(subset=columns_to_check, how='all')
    return data_sheet


def _drop_irrelevant_columns(data_sheet):
    data_sheet = data_sheet.drop(['Indicator Name', 'Indicator Code'], axis=1)
    columns_to_drop = [col for col in data_sheet.columns if
                       col.isdigit() and (1960 <= int(col) <= 1999 or int(col) >= 2022)]
    data_sheet = data_sheet.drop(columns=columns_to_drop, axis=1)
    return data_sheet


def _filter_countries(dataset, lac_country_codes):
    data_sheet = dataset.parse('Data', header=3)
    data_sheet = data_sheet[data_sheet['Country Code'].isin(lac_country_codes)]
    return data_sheet


def _get_country_codes(countries):
    lac_region = countries[countries['Region'] == 'Latin America & Caribbean']
    return list(lac_region['Country Code'])


def write_to_database(dataset1, dataset2):
    print('Writing to database...')
    remaining_countries = list(pd.merge(dataset1, dataset2, on='Country Code', how='inner')['Country Code'])

    dataset1 = dataset1[dataset1['Country Code'].isin(remaining_countries)]
    dataset2 = dataset2[dataset2['Country Code'].isin(remaining_countries)]

    try:
        conn = sqlite3.connect("../data/database.sqlite")
        dataset1.to_sql("life_expectancy", conn, if_exists="replace", index=False)
        dataset2.to_sql("health_expenditure", conn, if_exists="replace", index=False)
        conn.commit()
    except sqlite3.Error as e:
        print('Something went wrong during database connection.')
        raise Exception('Writing data failed', e)
    finally:
        conn.close()


if __name__ == '__main__':
    df1, df2 = download_datasets()
    filtered_dataset1 = clean_data(df1)
    filtered_dataset2 = clean_data(df2)
    write_to_database(filtered_dataset1, filtered_dataset2)
