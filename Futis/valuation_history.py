# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 13:07:24 2024

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
         SELECT p.name, p.player_id, pv.market_value_in_eur, pv.date
         FROM dbo.Players AS p
         JOIN dbo.PlayerValuations AS pv ON p.player_id = pv.player_id
         """)

# Read SQL query into a DataFrame
data = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Ensure the 'date' column is in datetime format
data['date'] = pd.to_datetime(data['date'])

# Convert market_value_in_eur to millions of euros
data['market_value_in_eur'] = data['market_value_in_eur'] / 1_000_000

# List of available players
all_players = data['name'].unique()
print(f"Available players: {', '.join(all_players)}")

# Prompt user to input player names, separated by commas
input_players = input("Enter player names separated by commas (exact match): ")

# Split the input into a list of player names
players_to_plot = [player.strip() for player in input_players.split(",")]

# Filter data for specific players
filtered_data = data[data['name'].isin(players_to_plot)]

# Check if there is any data to plot
if not filtered_data.empty:
    # Plotting
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=filtered_data, x='date', y='market_value_in_eur', hue='name', marker='o')

    plt.title('Market Value of Players Over Time')
    plt.xlabel('Date')
    plt.ylabel('Market Value (in M EUR)')
    plt.legend(title='Player Name')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()
else:
    print("No data found for the selected players. Please make sure to enter valid names.")


