# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:14:14 2024

@author: Heikki
"""

import pandas as pd
import pyodbc

# Load data to dataframe
data = pd.read_csv(r"C:\Users\Heikki\Documents/game_events.csv")
df = pd.DataFrame(data)

# Print DataFrame and Data Types for debugging
print("DataFrame:")
print(df)
print("\nData Types:")
print(df.dtypes)

# Ensure all relevant columns are of the correct type
df['game_id'] = pd.to_numeric(df['game_id'], errors='coerce').fillna(0).astype(int)
df['minute'] = pd.to_numeric(df['minute'], errors='coerce').fillna(0).astype(int)
df['club_id'] = pd.to_numeric(df['club_id'], errors='coerce').fillna(0).astype(int)
df['player_id'] = pd.to_numeric(df['player_id'], errors='coerce').fillna(0).astype(int)
df['player_in_id'] = pd.to_numeric(df['player_in_id'], errors='coerce').fillna(0).astype(int)
df['player_assist_id'] = pd.to_numeric(df['player_assist_id'], errors='coerce').fillna(0).astype(int)
df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
df['description'] = df['description'].fillna('')
df['description'] = df['description'].str.strip().str.replace(',', '')
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
    CREATE TABLE GameEvents (
    game_event_id nvarchar(50),              
    date nvarchar(50),            
    game_id int,                        
    minute int,                     
    type nvarchar(50),                        
    club_id int,                 
    player_id int,                
    description nvarchar(255),        
    player_in_id int,
    player_assist_id int                                                          

    
    )
    """
)

# Put data into the table from dataframe
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO GameEvents (game_event_id, date, game_id, minute, type, club_id, player_id, description, player_in_id, player_assist_id)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        row['game_event_id'],
        row['date'],
        row['game_id'],
        row['minute'],
        row['type'],
        row['club_id'],
        row['player_id'],
        row['description'],
        row['player_in_id'],
        row['player_assist_id']
        
    )
conn.commit()