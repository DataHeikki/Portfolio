# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 11:31:42 2024

@author: Heikki
"""

import pandas as pd
import pyodbc

# Load data to DataFrame
data = pd.read_csv(r"C:\Users\Heikki\Documents/transfers.csv")
df = pd.DataFrame(data)

# Print DataFrame and Data Types for debugging
print("DataFrame:")
print(df.head())
print("\nData Types:")
print(df.dtypes)

# Ensure all relevant columns are of the correct type
df['transfer_date'] = df['transfer_date'].astype(str)
df['player_id'] = pd.to_numeric(df['player_id'], errors='coerce').fillna(0).astype(int)
df['from_club_id'] = pd.to_numeric(df['from_club_id'], errors='coerce').fillna(0).astype(int)
df['to_club_id'] = pd.to_numeric(df['to_club_id'], errors='coerce').fillna(0).astype(int)
df['transfer_fee'] = pd.to_numeric(df['transfer_fee'], errors='coerce').fillna(0).astype(int)
df['market_value_in_eur'] = pd.to_numeric(df['market_value_in_eur'], errors='coerce').fillna(0).astype(int)
df['transfer_season'] = df['transfer_season'].fillna('Unknown')
df['from_club_name'] = df['from_club_name'].fillna('Unknown')
df['to_club_name'] = df['to_club_name'].fillna('Unknown')
df['player_name'] = df['player_name'].fillna('Unknown')

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
    CREATE TABLE Transfers (
   player_id int,                
   transfer_date nvarchar(50),          
   transfer_season nvarchar(50),        
   from_club_id int,            
   to_club_id int,
   from_club_name nvarchar(50),          
   to_club_name nvarchar(50),           
   transfer_fee int,          
   market_value_in_eur int,    
   player_name nvarchar(50),                 
    )
    """
)

#Put data to table from dataframe
for _, row in df.iterrows():  # iterrows() returns a tuple (index, Series)
    cursor.execute(
        """
        INSERT INTO Transfers (player_id, transfer_date, transfer_season, from_club_id, to_club_id, from_club_name, to_club_name, transfer_fee, market_value_in_eur, player_name)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        row['player_id'],  
        row['transfer_date'],
        row['transfer_season'],
        row['from_club_id'],
        row['to_club_id'],
        row['from_club_name'],
        row['to_club_name'],
        row['transfer_fee'],
        row['market_value_in_eur'],
        row['player_name'],
    )
conn.commit()