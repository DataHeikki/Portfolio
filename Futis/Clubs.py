# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 12:06:45 2024

@author: Heikki
"""

import pandas as pd
import pyodbc

# Load data to dataframe
data = pd.read_csv(r"C:\Users\Heikki\Documents/clubs.csv")
df = pd.DataFrame(data)

# Print DataFrame and Data Types for debugging
print("DataFrame:")
print(df)
print("\nData Types:")
print(df.dtypes)

# Ensure all relevant columns are of the correct type
df['club_id'] = pd.to_numeric(df['club_id'], errors='coerce').fillna(0).astype(int)
df['total_market_value'] = pd.to_numeric(df['total_market_value'], errors='coerce').fillna(0).astype(float)
df['squad_size'] = pd.to_numeric(df['squad_size'], errors='coerce').fillna(0).astype(int)
df['average_age'] = pd.to_numeric(df['average_age'], errors='coerce').fillna(0).astype(float)
df['foreigners_number'] = pd.to_numeric(df['foreigners_number'], errors='coerce').fillna(0).astype(int)
df['foreigners_percentage'] = pd.to_numeric(df['foreigners_percentage'], errors='coerce').fillna(0).astype(float)
df['national_team_players '] = pd.to_numeric(df['national_team_players'], errors='coerce').fillna(0).astype(int)
df['stadium_seats'] = pd.to_numeric(df['stadium_seats'], errors='coerce').fillna(0).astype(int)
df['coach_name'] = pd.to_numeric(df['coach_name'], errors='coerce').fillna(0).astype(float)
df['last_season'] = pd.to_numeric(df['last_season'], errors='coerce').fillna(0).astype(int)



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
    CREATE TABLE Clubs (
    club_id int,                    
    club_code nvarchar(50),                   
    name nvarchar(50),                         
    domestic_competition_id nvarchar(50),      
    total_market_value float,         
    squad_size int,
    average_age float,                
    foreigners_number int,            
    foreigners_percentage float,      
    national_team_players int,        
    stadium_name nvarchar(50),                 
    stadium_seats int,               
    net_transfer_record nvarchar(50),          
    coach_name float,                 
    last_season int,                                          

    
    )
    """
)

# Put data into the table from dataframe
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO Clubs (club_id, club_code, name, domestic_competition_id, total_market_value, squad_size, average_age, foreigners_number, foreigners_percentage, national_team_players, stadium_name, stadium_seats, net_transfer_record, coach_name, last_season)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        row['club_id'],
        row['club_code'],
        row['name'],
        row['domestic_competition_id'],
        row['total_market_value'],
        row['squad_size'],
        row['average_age'],
        row['foreigners_number'],
        row['foreigners_percentage'],
        row['national_team_players'],
        row['stadium_name'],
        row['stadium_seats'],
        row['net_transfer_record'],
        row['coach_name'],
        row['last_season'],
    )
conn.commit()