# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 11:07:22 2024

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

# Step 1: Query only player names (to avoid loading entire dataset)
query_players = "SELECT DISTINCT name FROM dbo.Players"
player_names_df = pd.read_sql(query_players, conn)

# List of available players
all_players = player_names_df['name'].unique()
print(f"Available players: {', '.join(all_players)}")

# Prompt user to input player names, separated by commas
input_players = input("Enter player names separated by commas (exact match): ")

# Split the input into a list of player names and format for SQL query
players_to_plot = [player.strip() for player in input_players.split(",")]

# Step 2: Modify SQL query to filter by selected players
# Use parameterized query to avoid SQL injection
query = f"""
         SELECT p.name, p.player_id, pv.market_value_in_eur, pv.date, a.goals, a.assists
         FROM dbo.Players AS p
         JOIN dbo.PlayerValuations AS pv ON p.player_id = pv.player_id
         JOIN dbo.Appereances AS a ON p.player_id = a.player_id
         WHERE p.name IN ({','.join('?' * len(players_to_plot))})
         """

# Step 3: Fetch data for selected players
data = pd.read_sql(query, conn, params=players_to_plot)

# Close the connection
conn.close()

# Ensure the 'date' column is in datetime format
data['date'] = pd.to_datetime(data['date'], errors='coerce')

# Check if there are any missing values after the conversion
if data['date'].isna().sum() > 0:
    print(f"Warning: {data['date'].isna().sum()} rows have invalid dates and were set to NaT.")

# Create the 'year' column by extracting year from the 'date' column
data['year'] = data['date'].dt.year

#Group data by player, year, and sum goals + assists, ensuring no duplication
# We group by player name, year, and use `sum` on goals and assists
trend_data = data.groupby(['name', 'year'], as_index=False).agg(
    total_goals=('goals', 'sum'),
    total_assists=('assists', 'sum')
)

#Calculate total goals + assists for each player per year
trend_data['total_goals_assists'] = trend_data['total_goals'] + trend_data['total_assists']

#Plot the trend for each player by year
plt.figure(figsize=(12, 6))
sns.lineplot(data=trend_data, x='year', y='total_goals_assists', hue='name', marker="o")

# Add plot labels and title
plt.title('Goals + Assists Trend by Year (Per Year Performance)')
plt.xlabel('Year')
plt.ylabel('Total Goals + Assists (Per Year)')
plt.xticks(rotation=45)
plt.legend(title='Player Name')

# Show plot
plt.tight_layout()
plt.show()

# Preview the trend data
print(trend_data)





