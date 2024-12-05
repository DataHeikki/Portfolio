# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 10:39:34 2024

@author: Heikki
"""

import pandas as pd
import pyodbc

# Load data to DataFrame
data = pd.read_csv(r"C:\Users\Heikki\Documents/player_valuations.csv")
df = pd.DataFrame(data)

# Print DataFrame and Data Types for debugging
print("DataFrame:")
print(df.head())
print("\nData Types:")
print(df.dtypes)


# Ensure all relevant columns are of the correct type
df['date'] = df['date'].astype(str)
df['player_id'] = pd.to_numeric(df['player_id'], errors='coerce').fillna(0).astype(int)
df['market_value_in_eur'] = pd.to_numeric(df['market_value_in_eur'], errors='coerce').fillna(0).astype(int)
df['current_club_id'] = pd.to_numeric(df['current_club_id'], errors='coerce').fillna(0).astype(int)
df['player_club_domestic_competition_id'] = df['player_club_domestic_competition_id'].fillna('Unknown')

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
    CREATE TABLE PlayerValuations (
    player_id int,                              
    date nvarchar(50),                                   
    market_value_in_eur int,                     
    current_club_id int,                         
    player_club_domestic_competition_id nvarchar(50),    
    )
    """
)

#Put data to table from dataframe
for _, row in df.iterrows():  # iterrows() returns a tuple (index, Series)
    cursor.execute(
        """
        INSERT INTO PlayerValuations (player_id, date, market_value_in_eur, current_club_id, player_club_domestic_competition_id)
        VALUES (?,?,?,?,?)
        """,
        row['player_id'],  
        row['date'],
        row['market_value_in_eur'],
        row['current_club_id'],
        row['player_club_domestic_competition_id'],
    )
conn.commit()

