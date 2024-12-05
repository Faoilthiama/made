import importlib.util
import os
import sqlite3
import subprocess
import tempfile
import tracemalloc
import unittest
import urllib.request
from io import StringIO
from unittest.mock import Mock, patch
from urllib import request
from urllib.error import URLError

import pandas as pd

FILE_PATH = "data-pipeline.py"
DATA_PATH = "test-data.xls"

spec = importlib.util.spec_from_file_location("data_pipeline", FILE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SystemTest(unittest.TestCase):
    def test_that_pipeline_creates_database(self):
        path = '../data/database.sqlite'
        if os.path.exists(path):
            os.remove(path)

        result = subprocess.run(["python", "data-pipeline.py"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(path))

        os.remove(path)


class TestDownload(unittest.TestCase):

    def setUp(self):
        self.path1 = './dataset1.xls'
        self.path2 = './dataset2.xls'
        if os.path.exists(self.path1):
            os.remove(self.path1)
        if os.path.exists(self.path2):
            os.remove(self.path2)

    def tearDown(self):
        if os.path.exists(self.path1):
            os.remove(self.path1)
        if os.path.exists(self.path2):
            os.remove(self.path2)

    def test_download_create_files(self):
        # Arrange
        request.urlretrieve = Mock(side_effect=self.mock_urlretrieve)

        # Act
        module.download_datasets()

        # Assert
        self.assertTrue(os.path.exists(self.path1))
        self.assertTrue(os.path.exists(self.path2))

    def test_download_return_value_not_empty(self):
        # Arrange
        request.urlretrieve = Mock(side_effect=self.mock_urlretrieve)

        # Act
        df1, df2 = module.download_datasets()

        # Assert
        self.assertNotEqual(df1, None)
        self.assertNotEqual(df2, None)

    @patch("sys.stdout", new_callable=StringIO)
    def test_download_retry(self, mock_stdout):
        # Arrange
        request.urlretrieve = Mock(side_effect=URLError('test'))

        # Act
        with self.assertRaises(Exception):
            module.download_datasets()

        # Assert
        output = mock_stdout.getvalue()
        self.assertIn("Retrying for the 1. time.", output)
        self.assertIn("Retrying for the 2. time.", output)
        self.assertIn("Aborting pipeline due to too many failed download attempts.", output)

    @staticmethod
    def mock_urlretrieve(url, filename):
        with open('test-data.xls', "rb") as src_file, open(filename, "wb") as dest_file:
            dest_file.write(src_file.read())


class TestWriteDatabase(unittest.TestCase):

    def setUp(self):
        self.path = '../data/database.sqlite'
        if os.path.exists(self.path):
            os.remove(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_write_database_create_file(self):
        # Arrange
        df = pd.ExcelFile(DATA_PATH)
        data1 = df.parse('Data', header=3)
        data2 = df.parse('Data', header=3)

        # Act
        module.write_to_database(data1, data2)

        # Assert
        self.assertTrue(os.path.exists(self.path))

    def test_write_database_contains_correct_tables(self):
        # Arrange
        df = pd.ExcelFile(DATA_PATH)
        df = pd.ExcelFile(DATA_PATH)
        data1 = df.parse('Data', header=3)
        data2 = df.parse('Data', header=3)

        # Act
        module.write_to_database(data1, data2)

        # Assert
        try:
            conn = sqlite3.connect(self.path)
            cursor = conn.cursor()
            sql_query = ".tables"
            cursor.execute(sql_query)
            tables = cursor.fetchall()

            self.assertTrue(len(tables) == 2)
            self.assertTrue("life_expectancy" in tables)
            self.assertTrue("health_expenditure" in tables)
        except sqlite3.Error:
            print('Something went wrong during database connection.')


class TestCleanData(unittest.TestCase):
    def test_get_country_codes(self):
        # Arrange
        df = pd.ExcelFile(DATA_PATH)
        countries = df.parse('Metadata - Countries')

        # Act
        country_codes = module._get_country_codes(countries)

        # Assert
        self.assertFalse("TEST" in country_codes)
        self.assertFalse("AFG" in country_codes)
        self.assertTrue("ARG" in country_codes)

    def test_filter_countries(self):
        # Arrange
        df = pd.ExcelFile(DATA_PATH)

        # Act
        actual = module._filter_countries(df, ['ARG'])

        # Assert
        self.assertTrue("ARG" in actual['Country Code'].values)
        self.assertFalse("TEST" in actual['Country Code'].values)

    def test_drop_irrelevant_columns(self):
        # Arrange
        df = pd.ExcelFile(DATA_PATH)
        data = df.parse('Data', header=3)

        # Act
        actual = module._drop_irrelevant_columns(data)

        # Assert
        self.assertFalse("Indicator Name" in actual.columns)
        self.assertFalse("Indicator Code" in actual.columns)
        self.assertFalse("1975" in actual.columns)
        self.assertTrue("2010" in actual.columns)

    def test_drop_empty_rows(self):
        # Arrange
        df = pd.ExcelFile(DATA_PATH)
        data = df.parse('Data', header=3)

        # Act
        actual = module._drop_empty_rows(data)

        # Assert
        self.assertFalse("EMPTY" in actual['Country Code'].values)
        self.assertTrue("ARG" in actual['Country Code'].values)

    def test_clean_data_fills_missing_values(self):
        # Arrange
        file = pd.ExcelFile(DATA_PATH)

        # Act
        actual = module.clean_data(file)

        # Assert
        self.assertTrue("BLZ" in actual['Country Code'].values)
        self.assertFalse(actual.isnull().any().any())
