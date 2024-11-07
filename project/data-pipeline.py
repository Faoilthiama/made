import urllib.request
import pandas as pd
import sqlite3

DATASET1 = "dataset1.xls"
DATASET2 = "dataset2.xls"


def download_datasets():
    print('Downloading datasets...')
    urllib.request.urlretrieve("https://api.worldbank.org/v2/en/indicator/SP.DYN.LE00.IN?downloadformat=excel",
                               DATASET1)
    urllib.request.urlretrieve("https://api.worldbank.org/v2/en/indicator/SH.XPD.CHEX.PP.CD?downloadformat=excel",
                               DATASET2)


def clean_data(dataset: str):
    print(f'Cleaning data in {dataset}...')
    df = pd.ExcelFile(dataset)
    countries = df.parse('Metadata - Countries')
    lac_region = countries[countries['Region'] == 'Latin America & Caribbean']
    lac_country_codes = list(lac_region['Country Code'])

    data_sheet = df.parse('Data', header=3)
    data_sheet = data_sheet[data_sheet['Country Code'].isin(lac_country_codes)]
    return data_sheet.drop(['Indicator Name', 'Indicator Code'], axis=1)


def write_to_database(dataset1, dataset2):
    print('Writing to database...')
    conn = sqlite3.connect("../data/database.sqlite")
    dataset1.to_sql("life_expectancy", conn, if_exists="replace", index=False)
    dataset2.to_sql("health_expenditure", conn, if_exists="replace", index=False)


if __name__ == '__main__':
    download_datasets()
    filtered_dataset1 = clean_data(DATASET1)
    filtered_dataset2 = clean_data(DATASET2)
    write_to_database(filtered_dataset1, filtered_dataset2)
