# function that cleans database files and exports them to a CSV
import sqlite3 as s3
import pandas as pd

db_name = input("Please input name of database file, do not include extention. ")
con = s3.connect(f'{db_name}.db')


def clean_loader(db_con_file):
    cur = db_con_file.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cur.fetchall()]

    for table in tables:

        # generates dataframe for cleaning
        df = pd.read_sql_query(f"SELECT * FROM {table}", db_con_file)

        # step removes duplicates prints string if it did, and if it didn't it also returns a string
        if (len(df)) - len(df.drop_duplicates()) > 0:
            df = df.drop_duplicates()
            print('duplicates dropped')
        if (len(df)) - len(df.drop_duplicates()) == 0:
            print('table has no duplicates')

        # removes NaN values and returns string if it didn't
        if df.isna().values.any() == True:
            df = df.dropna()
            print('NaN rows dropped')
        else:
            ('No NaN values')

        df.to_csv(f"{table}_cleaned.csv", index=False)
        print(f"{table}_cleaned.csv was created")

clean_loader(con)
con.close()