
import sqlite3

import pandas as pd


def insert(filter_list):
    with sqlite3.connect("test.db") as conn:
            cursor = conn.cursor()
            statement = '''
            INSERT OR IGNORE INTO city(id,name,city_ascii,lat,lng,country,iso2,iso3,admin_name,capital,population)
            VALUES
                (?,?,?,?,?,?,?,?,?,?,?)'''
            cursor.execute(statement, filter_list)
def test():
     with sqlite3.connect("test.db") as conn:
            cursor = conn.cursor()
            statement = '''
            SELECT * FROM user'''
            cursor.execute(statement)
            return cursor.fetchall()
def clean():
    with sqlite3.connect("test.db") as conn:
            cursor = conn.cursor()
            statement = '''
            DELETE FROM city'''
            cursor.execute(statement)
def clean2():
    with sqlite3.connect("test.db") as conn:
            cursor = conn.cursor()
            statement = '''
            DELETE FROM ticket_passenger'''
            cursor.execute(statement)
def check_data():
    city_data = pd.read_csv("worldcities.csv")
    for i in range(11):
        print(city_data[city_data.columns[i]].isnull().values.any())

def main():
    clean2()
    # clean()
    # # for i in range(5):
    # #     print(type(test()[0][i]))
    # #print(test())

    # city_data = pd.read_csv("worldcities.csv")
    # city_data = city_data.dropna()
    # city_data.reset_index(drop=True, inplace=True)
    # for i in range(len(city_data.index)):
    #     filter_list = [city_data.loc[i][k] for k in range(10)]
    #     filter_list.insert(0,city_data.loc[i][10])
    #     # convert np.int to int, np.float to float
    #     filter_list[0] = int(filter_list[0])
    #     filter_list[3] = float(filter_list[3])
    #     filter_list[4] = float(filter_list[4])
    #     filter_list[10] = int(filter_list[10])
    #     insert(filter_list)

if __name__ == '__main__':
    main()
