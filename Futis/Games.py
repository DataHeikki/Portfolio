# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 12:45:06 2024

@author: Heikki
"""

import pandas as pd
import pyodbc

# Load data to DataFrame
data = pd.read_csv(r"C:\Users\Heikki\Documents/games.csv")
df = pd.DataFrame(data)

# Print DataFrame and Data Types for debugging
print("DataFrame:")
print(df.head())
print("\nData Types:")
print(df.dtypes)

# Ensure all relevant columns are of the correct type
df['home_club_position'] = pd.to_numeric(df['home_club_position'], errors='coerce').fillna(0).astype(int)
df['away_club_position'] = pd.to_numeric(df['away_club_position'], errors='coerce').fillna(0).astype(int)
df['attendance'] = pd.to_numeric(df['attendance'], errors='coerce').fillna(0).astype(int)
df['date'] = df['date'].astype(str)
df['round'] = df['round'].astype(str)
df['season'] = df['season'].astype(str)
df['aggregate'] = df['aggregate'].astype(str)
df['home_club_formation'] = df['home_club_formation'].fillna('Unknown').astype(str)
df['away_club_formation'] = df['away_club_formation'].fillna('Unknown').astype(str)
df['referee'] = df['referee'].fillna('Unknown')
df['stadium'] = df['stadium'].fillna('Unknown')
df['home_club_name'] = df['home_club_name'].fillna('Unknown')
df['away_club_name'] = df['away_club_name'].fillna('Unknown')
df['away_club_manager_name'] = df['away_club_manager_name'].fillna('Unknown')
df['home_club_manager_name'] = df['home_club_manager_name'].fillna('Unknown')

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

    CREATE TABLE Games (
        game_id bigint PRIMARY KEY,                     
        competition_id nvarchar(255),            
        season nvarchar(50),                     
        round nvarchar(50),                     
        date nvarchar(50),                      
        home_club_id bigint,              
        away_club_id bigint,                
        home_club_goals int,             
        away_club_goals int,             
        home_club_position int,        
        away_club_position int,       
        home_club_manager_name nvarchar(255),       
        away_club_manager_name nvarchar(255),      
        stadium nvarchar(255),                      
        attendance int,             
        referee nvarchar(50),                                            
        home_club_formation nvarchar(50),         
        away_club_formation nvarchar(50),         
        home_club_name nvarchar(255),              
        away_club_name nvarchar(255),               
        aggregate nvarchar(50),                   
        competition_type nvarchar(50),             
    )
    """
)

# Insert data into the table
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO Games (game_id, competition_id, season, round, date, home_club_id, away_club_id, home_club_goals, away_club_goals, home_club_position, away_club_position, home_club_manager_name, away_club_manager_name, stadium, attendance, referee, home_club_formation, away_club_formation, home_club_name, away_club_name, aggregate, competition_type)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        row['game_id'],
        row['competition_id'],
        row['season'],
        row['round'],
        row['date'],
        row['home_club_id'],
        row['away_club_id'],
        row['home_club_goals'],
        row['away_club_goals'],
        row['home_club_position'],
        row['away_club_position'],
        row['home_club_manager_name'],
        row['away_club_manager_name'],
        row['stadium'],
        row['attendance'],
        row['referee'],
        row['home_club_formation'],
        row['away_club_formation'],
        row['home_club_name'],
        row['away_club_name'],
        row['aggregate'],
        row['competition_type']
    )
conn.commit()