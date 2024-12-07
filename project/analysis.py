import os
import shutil
import sqlite3
import subprocess

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


def descriptive_analysis():
    life_expectancy, health_expenditure = _load_datasets()
    columns = [str(x) for x in range(2000, 2022)]
    # _plot_mean_graph(life_expectancy, health_expenditure, columns)
    # _compute_ranges(life_expectancy, health_expenditure)
    _scatter_graph(life_expectancy, health_expenditure, columns)


def _load_datasets():
    conn = sqlite3.connect('../data/database.sqlite')

    life_expectancy = pd.read_sql_query("SELECT * FROM life_expectancy", conn)
    health_expenditure = pd.read_sql_query("SELECT * FROM health_expenditure", conn)

    return life_expectancy, health_expenditure


def _plot_mean_graph(life_expectancy, health_expenditure, columns):
    mean_life_expectancy = life_expectancy[columns].mean()
    mean_health_expenditure = health_expenditure[columns].mean()

    fig, ax1 = plt.subplots()

    x = range(2000, 2022)

    ax1.plot(x, mean_life_expectancy, label='Mean life expectancy', color='blue')

    ax2 = ax1.twinx()
    ax2.plot(x, mean_health_expenditure, label='Mean health expenditure', color='orange')

    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.1))

    plt.show()


def _scatter_graph(life_expectancy, health_expenditure, columns):
    output_directory = "../data/plots"

    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.makedirs(output_directory)

    df = pd.merge(life_expectancy, health_expenditure, on=['Country Code', 'Country Name'])
    countries = life_expectancy['Country Code']


    for country in countries:
        country_data = df[df['Country Code'] == country]
        plt.figure(figsize=(10, 6))
        all_health_expenditure = []
        all_life_expectancy = []
        for year in columns:
            x = country_data[year + '_y'],
            y = country_data[year + '_x'],
            plt.scatter(
                x,
                y,
                label=f'{year}',
                color='blue',
                alpha=0.7,
                s=100,
                edgecolor='black'
            )
            all_health_expenditure.extend(x[0])
            all_life_expectancy.extend(y[0])
        coefficients = np.polyfit(all_health_expenditure, all_life_expectancy, 1)
        trendline = np.polyval(coefficients, np.array(all_health_expenditure))

        # Plot the global trendline
        plt.plot(all_health_expenditure, trendline, color='black', linestyle='-', label='Trendline (All Years)')

        plt.xlabel('Health Expenditure per Capita')
        plt.ylabel('Life Expectancy at Birth')
        plt.title('Health Expenditure vs Life Expectancy for Each Country by Year')

        plot_filename = os.path.join(output_directory, f"{country.replace(' ', '_')}_plot.png")
        plt.tight_layout()
        plt.savefig(plot_filename)
        plt.close()


def _compute_ranges(life_expectancy, health_expenditure):
    countries = life_expectancy[['Country Code']]
    life_expectancy_years = life_expectancy.drop(['Country Name', 'Country Code'], axis=1)
    health_expenditure_years = health_expenditure.drop(['Country Name', 'Country Code'], axis=1)
    min_life_expectancy = life_expectancy_years.min(axis=1)
    max_life_expectancy = life_expectancy_years.max(axis=1)
    min_health_expenditure = health_expenditure_years.min(axis=1)
    max_health_expenditure = health_expenditure_years.max(axis=1)

    for i in range(len(countries)):
        country = countries.iloc[i].item()  # Clean scalar value
        min_val = min_life_expectancy.iloc[i].item()
        max_val = max_life_expectancy.iloc[i].item()

        print(f'Range of life expectancy for {country}: [{min_val:.3f}; {max_val:.3f}]')

    for i in range(len(countries)):
        country = countries.iloc[i].item()  # Clean scalar value
        min_val = min_health_expenditure.iloc[i].item()
        max_val = max_health_expenditure.iloc[i].item()

        print(f'Range of health expenditure for {country}: [{min_val:.3f}; {max_val:.3f}]')


if __name__ == "__main__":
    # subprocess.call("./pipeline.sh")
    descriptive_analysis()
