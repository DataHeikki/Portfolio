# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 10:55:56 2024

@author: Heikki
"""

import pandas as pd
import pyodbc

# Load data to DataFrame
data = pd.read_csv(r"C:\Users\Heikki\Documents/players.csv")
df = pd.DataFrame(data)

# Print DataFrame and Data Types for debugging
print("DataFrame:")
print(df.head())
print("\nData Types:")
print(df.dtypes)

# Ensure all relevant columns are of the correct type
df['date_of_birth'] = df['date_of_birth'].astype(str)
df['contract_expiration_date'] = df['contract_expiration_date'].astype(str)
df['player_id'] = pd.to_numeric(df['player_id'], errors='coerce').fillna(0).astype(int)
df['last_season'] = pd.to_numeric(df['last_season'], errors='coerce').fillna(0).astype(int)
df['current_club_id'] = pd.to_numeric(df['current_club_id'], errors='coerce').fillna(0).astype(int)
df['height_in_cm'] = pd.to_numeric(df['height_in_cm'], errors='coerce').fillna(0).astype(int)
df['highest_market_value_in_eur'] = pd.to_numeric(df['highest_market_value_in_eur'], errors='coerce').fillna(0).astype(int)
df['market_value_in_eur'] = pd.to_numeric(df['market_value_in_eur'], errors='coerce').fillna(0).astype(int)
df['first_name'] = df['first_name'].fillna('Unknown')
df['last_name'] = df['last_name'].fillna('Unknown')
df['name'] = df['name'].fillna('Unknown')
df['player_code'] = df['player_code'].fillna('Unknown')
df['country_of_birth'] = df['country_of_birth'].fillna('Unknown')
df['city_of_birth'] = df['city_of_birth'].fillna('Unknown')
df['country_of_citizenship'] = df['country_of_citizenship'].fillna('Unknown')
df['sub_position'] = df['sub_position'].fillna('Unknown')
df['position'] = df['position'].fillna('Unknown')
df['foot'] = df['foot'].fillna('Unknown')
df['agent_name'] = df['agent_name'].fillna('Unknown')
df['current_club_domestic_competition_id'] = df['current_club_domestic_competition_id'].fillna('Unknown')
df['current_club_name'] = df['current_club_name'].fillna('Unknown')

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
    CREATE TABLE Players (
    player_id int,                                 
    first_name nvarchar(50),                               
    last_name nvarchar(50),                                
    name nvarchar(50),                                     
    last_season int,
    current_club_id int,                          
    player_code nvarchar(50),                              
    country_of_birth nvarchar(50),                         
    city_of_birth nvarchar(255),                            
    country_of_citizenship nvarchar(50),                   
    date_of_birth nvarchar(50),                            
    sub_position nvarchar(50),                             
    position nvarchar(50),                                 
    foot nvarchar(50),                                     
    height_in_cm int,                           
    contract_expiration_date nvarchar(50),                 
    agent_name nvarchar(50),                                                                  
    current_club_domestic_competition_id nvarchar(50),     
    current_club_name nvarchar(50),                        
    market_value_in_eur int,                     
    highest_market_value_in_eur int,               
    )
    """
)

#Put data to table from dataframe
for _, row in df.iterrows():  # iterrows() returns a tuple (index, Series)
    cursor.execute(
        """
        INSERT INTO Players (player_id, first_name, last_name, name, last_season, current_club_id, player_code, 
        country_of_birth, city_of_birth, country_of_citizenship, date_of_birth, sub_position, position, foot, 
        height_in_cm, contract_expiration_date, agent_name, current_club_domestic_competition_id, current_club_name, market_value_in_eur, highest_market_value_in_eur)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        row['player_id'],  
        row['first_name'],
        row['last_name'],
        row['name'],
        row['last_season'],
        row['current_club_id'],
        row['player_code'],
        row['country_of_birth'],
        row['city_of_birth'],
        row['country_of_citizenship'],
        row['date_of_birth'],
        row['sub_position'],
        row['position'],
        row['foot'],
        row['height_in_cm'],
        row['contract_expiration_date'],
        row['agent_name'],
        row['current_club_domestic_competition_id'],
        row['current_club_name'],
        row['market_value_in_eur'],
        row['highest_market_value_in_eur'],
    )
conn.commit()
