# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 12:48:51 2024

@author: Heikki
"""

import pandas as pd
import pyodbc

# Load data to dataframe
data = pd.read_csv(r"C:\Users\Heikki\Documents/competitions.csv")
df = pd.DataFrame(data)

# Print DataFrame and Data Types for debugging
print("DataFrame:")
print(df)
print("\nData Types:")
print(df.dtypes)

# Ensure all relevant columns are of the correct type
df['country_id'] = pd.to_numeric(df['country_id'], errors='coerce').fillna(0).astype(int)
df['is_major_national_league'] = pd.to_numeric(df['is_major_national_league'], errors='coerce').fillna(0).astype(int)
df['country_name'] = df['country_name'].fillna('Unknown')
df['domestic_league_code'] = df['domestic_league_code'].fillna('N/A')



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
    CREATE TABLE Competitions (
    competition_id nvarchar(50),              
    competition_code nvarchar(50),            
    name nvarchar(50),                        
    sub_type nvarchar(50),                     
    type nvarchar(50),                        
    country_id int,                 
    country_name nvarchar(50),                
    domestic_league_code nvarchar(50),        
    confederation nvarchar(50),
    is_major_national_league int                                                          

    
    )
    """
)

# Put data into the table from dataframe
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO Competitions (competition_id, competition_code, name, sub_type, type, country_id, country_name, domestic_league_code, confederation, is_major_national_league)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        row['competition_id'],
        row['competition_code'],
        row['name'],
        row['sub_type'],
        row['type'],
        row['country_id'],
        row['country_name'],
        row['domestic_league_code'],
        row['confederation'],
        row['is_major_national_league']
        
    )
conn.commit()