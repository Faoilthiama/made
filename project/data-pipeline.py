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

    data_sheet.drop(['Indicator Name', 'Indicator Code'], axis=1, inplace=True)
    columns_to_drop = [col for col in data_sheet.columns if col.isdigit() and (1960 <= int(col) <= 1999 or int(col) >= 2022)]
    data_sheet.drop(columns=columns_to_drop, axis=1, inplace=True)

    columns_to_check = [str(year) for year in range(2000, 2022)]
    data_sheet = data_sheet.dropna(subset=columns_to_check, how='all')
    return data_sheet.fillna(0)



def write_to_database(dataset1, dataset2):
    print('Writing to database...')
    remaining_countries = list(pd.merge(dataset1, dataset2, on='Country Code', how='inner')['Country Code'])

    dataset1 = dataset1[dataset1['Country Code'].isin(remaining_countries)]
    dataset2 = dataset2[dataset2['Country Code'].isin(remaining_countries)]

    conn = sqlite3.connect("../data/database.sqlite")
    dataset1.to_sql("life_expectancy", conn, if_exists="replace", index=False)
    dataset2.to_sql("health_expenditure", conn, if_exists="replace", index=False)


if __name__ == '__main__':
    download_datasets()
    filtered_dataset1 = clean_data(DATASET1)
    filtered_dataset2 = clean_data(DATASET2)
    write_to_database(filtered_dataset1, filtered_dataset2)
