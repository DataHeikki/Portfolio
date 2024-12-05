# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 12:36:41 2024

@author: Heikki
"""

import pandas as pd
import pyodbc


# Load data to dataframe
data = pd.read_csv(r"C:\Users\Heikki\Documents/appearances.csv")
df = pd.DataFrame(data)

print(df)

# Connection to Database
conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost\\SQLEXPRESS;"
    "Database=FootballDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes"
)
cursor = conn.cursor()

# Create Table
cursor.execute(
    """
    CREATE TABLE appereances (
    appearance_id nvarchar(50) primary key,
    game_id nvarchar(50),
    player_id nvarchar(50),
    goals int,
    assists int,
    minutes_played int
    )
    """
)

#Put data to table from dataframe
for _, row in df.iterrows():  # iterrows() returns a tuple (index, Series)
    cursor.execute(
        """
        INSERT INTO appereances (appearance_id, game_id, player_id, goals, assists, minutes_played)
        VALUES (?,?,?,?,?,?)
        """,
        row['appearance_id'],  # Access column using the column name
        row['game_id'],
        row['player_id'],
        row['goals'],
        row['assists'],
        row['minutes_played']
    )
conn.commit()