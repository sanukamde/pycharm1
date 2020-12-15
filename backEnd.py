# Author: Sanika Kamde / Lab 1

import re
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


class Temperature:
    def __init__(self, year, median):
        self.year = year
        self.median = median

    def __str__(self):
        return str(self.year) + " " + str(self.median)


class Backend:
    def __init__(self):
        self.table_connect = sqlite3.connect('temp_table.db')
        self.year = []
        self.median = []

    def build_SQLite_table(self):
        temp_table_create_query = '''CREATE TABLE IF NOT EXISTS Database (id INTEGER PRIMARY KEY, year INTEGER,
        median REAL); '''
        self.table_connect.execute(temp_table_create_query)

    def close_SQLite_table(self):
        self.table_connect.close()

    def graph_builder(self):
        cursor = self.table_connect.execute("SELECT id, year, median from Database")
        for row in cursor:
            self.year.append(row[1])
            self.median.append(row[2])

    def insert(self, file):
        html_file = open(file)
        regex = re.compile("-?\d*\.?\d+")
        insert_data_query = '''INSERT OR IGNORE INTO Database (id, year, median) VALUES (?,?,?) '''
        id_count = 0
        for line in html_file:
            data = regex.findall(line)
            if len(data) <= 2:
                continue
            if int(data[0]) < 1960 or int(data[0]) > 1990:
                continue
            # if float(data[1]) < 0:
            #     continue
            data_tuple = (id_count, int(data[0]), float(data[1]))
            id_count += 1
            self.table_connect.execute(insert_data_query, data_tuple)
        self.graph_builder()
        self.table_connect.commit()

    def build_xy_plot(self):
        plt.plot(self.year, self.median, '-')
        plt.ylabel('Median Value (°C)')
        plt.xlabel('Year')
        plt.axhline(y=0, linestyle='--', color='red')  # shows
        plt.grid()
        plt.show()

    def build_bar_chart(self):
        plt.bar(self.year, self.median, color='green')
        plt.ylabel('Median Value (°C)')
        plt.xlabel('Year')
        plt.axhline(y=0, linestyle='--', color='red')  # shows
        plt.grid()
        plt.show()

    def build_linear_regression(self):
        df = pd.read_sql_query("SELECT id, year, median from Database", self.table_connect)
        X = df.iloc[:, 1].values.reshape(-1, 1)
        Y = df.iloc[:, 2].values.reshape(-1, 1)
        linear_regressor = LinearRegression()
        linear_regressor.fit(X, Y)
        Y_pred = linear_regressor.predict(X)
        plt.ylabel('Median Value (°C)')
        plt.xlabel('Year')
        plt.scatter(X, Y, color='purple')
        plt.plot(X, Y_pred, color='red')
        plt.show()
