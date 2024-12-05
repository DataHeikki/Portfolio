# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 12:13:43 2024

@author: Heikki
"""

import pandas as pd
import pyodbc

# Load data to DataFrame
data = pd.read_csv(r"C:\Users\Heikki\Documents/game_lineups.csv")
df = pd.DataFrame(data)

# Print DataFrame and Data Types for debugging
print("DataFrame:")
print(df.head())
print("\nData Types:")
print(df.dtypes)

# Ensure all relevant columns are of the correct type
df['game_lineups_id'] = df['game_lineups_id'].fillna('')
df['player_name'] = df['player_name'].fillna('')
df['type'] = df['type'].fillna('')
df['position'] = df['position'].fillna('')
df['number'] = df['number'].fillna('').astype(str)  # Convert number to string to accommodate all possible values
df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')

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
    IF OBJECT_ID('GameLineups', 'U') IS NOT NULL 
    DROP TABLE GameLineups;

    CREATE TABLE GameLineups (
        game_lineups_id nvarchar(50),
        date nvarchar(50),
        game_id int,
        player_id int,
        club_id int,
        player_name nvarchar(50),
        type nvarchar(255),
        position nvarchar(50),
        number nvarchar(50),
        team_captain int
    )
    """
)

# Insert data into the table
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO GameLineups (game_lineups_id, date, game_id, player_id, club_id, player_name, type, position, number, team_captain)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        row['game_lineups_id'],
        row['date'],
        row['game_id'],
        row['player_id'],
        row['club_id'],
        row['player_name'],
        row['type'],
        row['position'],
        row['number'],
        row['team_captain']
    )
conn.commit()


