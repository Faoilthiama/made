import sqlite3

import pandas as pd


def load_datasets():
    conn = sqlite3.connect('../../data/database.sqlite')

    life_expectancy = pd.read_sql_query("SELECT * FROM life_expectancy", conn)
    health_expenditure = pd.read_sql_query("SELECT * FROM health_expenditure", conn)

    return life_expectancy, health_expenditure