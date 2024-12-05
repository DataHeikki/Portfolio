# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 11:02:47 2024

@author: Heikki
"""

import pandas as pd
import pyodbc

# Load data to dataframe
data = pd.read_csv(r"C:\Users\Heikki\Documents/club_games.csv")
df = pd.DataFrame(data)

# Print DataFrame and Data Types for debugging
print("DataFrame:")
print(df)
print("\nData Types:")
print(df.dtypes)

# Convert columns to appropriate types and handle missing values
# Ensure all relevant columns are of the correct type
df['game_id'] = pd.to_numeric(df['game_id'], errors='coerce').fillna(0).astype(int)
df['club_id'] = pd.to_numeric(df['club_id'], errors='coerce').fillna(0).astype(int)
df['own_goals'] = pd.to_numeric(df['own_goals'], errors='coerce').fillna(0).astype(int)
df['own_position'] = pd.to_numeric(df['own_position'], errors='coerce').fillna(0).astype(float)
df['opponent_id'] = pd.to_numeric(df['opponent_id'], errors='coerce').fillna(0).astype(int)
df['opponent_goals'] = pd.to_numeric(df['opponent_goals'], errors='coerce').fillna(0).astype(int)
df['opponent_position'] = pd.to_numeric(df['opponent_position'], errors='coerce').fillna(0).astype(float)
df['is_win'] = pd.to_numeric(df['is_win'], errors='coerce').fillna(0).astype(int)

# Handle any missing values by replacing NaNs with default values if necessary
df.fillna({
    'own_manager_name': '',
    'opponent_manager_name': '',
    'hosting': ''
}, inplace=True)

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
    CREATE TABLE ClubGames (
    game_id int,
    club_id int,
    own_goals int,
    own_position float,
    own_manager_name nvarchar(50),
    opponent_id int,
    opponent_goals int,
    opponent_position float,
    opponent_manager_name nvarchar(50),
    hosting nvarchar(50),
    is_win int
    )
    """
)

# Put data into the table from dataframe
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO ClubGames (game_id, club_id, own_goals, own_position, own_manager_name, opponent_id, opponent_goals, opponent_position, opponent_manager_name, hosting, is_win)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,
        row['game_id'],
        row['club_id'],
        row['own_goals'],
        row['own_position'],
        row['own_manager_name'],
        row['opponent_id'],
        row['opponent_goals'],
        row['opponent_position'],
        row['opponent_manager_name'],
        row['hosting'],
        row['is_win']
    )
conn.commit()

# Check for missing values again after operations
print("\nMissing Values After Operations:")
print(df.isna().sum())
