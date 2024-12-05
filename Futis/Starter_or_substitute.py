# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 10:34:31 2024

@author: Heikki
"""

import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connection to Database
conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost\\SQLEXPRESS;"
    "Database=FootballDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes"
)

# Query to get data
query = ("""
         SELECT player_name, type 
         FROM dbo.GameLineups
         """)

# Read SQL query into a DataFrame
data = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Preview the DataFrame
print(data.head())

# Input the player name to filter
player_name_input = input("Enter player name: ")

# Filter the data for the specific player
player_data = data[data['player_name'] == player_name_input]

if not player_data.empty:
    # Group by player_name and type, then count occurrences for the specific player
    grouped_data = player_data.groupby(['player_name', 'type']).size().unstack(fill_value=0)

    # Calculate total games for the player
    grouped_data['total_games'] = grouped_data.sum(axis=1)

    # Calculate percentage for starter and substitute
    grouped_data['starter_percent'] = (grouped_data.get('starting_lineup', 0) / grouped_data['total_games']) * 100
    grouped_data['substitute_percent'] = (grouped_data.get('substitutes', 0) / grouped_data['total_games']) * 100

    # Preview the data
    print(grouped_data[['starter_percent', 'substitute_percent']])

    # Visualization using seaborn
    plt.figure(figsize=(8, 6))
    sns.barplot(x=['Starter %', 'Substitute %'], y=[grouped_data['starter_percent'].values[0], grouped_data['substitute_percent'].values[0]], palette='viridis')

    plt.ylabel('Percentage of Games')
    plt.title(f'Percentage of Games Played as Starter and Substitute for {player_name_input}')
    plt.tight_layout()
    plt.show()
else:
    print(f"No data found for player: {player_name_input}")



