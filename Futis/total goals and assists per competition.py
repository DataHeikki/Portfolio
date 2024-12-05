# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 12:07:43 2024

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
query = f"""
    SELECT 
        p.name AS player_name, 
        c.name AS competition_name, 
        SUM(a.goals) AS total_goals, 
        SUM(a.assists) AS total_assists,
        COUNT(g.game_id) AS total_games
    FROM dbo.Players AS p
    JOIN dbo.Appereances AS a ON p.player_id = a.player_id
    JOIN dbo.Games AS g ON a.game_id = g.game_id
    JOIN dbo.Competitions AS c ON g.competition_id = c.competition_id
    WHERE p.name IN ({','.join('?' * len(players_to_plot))})
    GROUP BY p.name, c.name
    ORDER BY p.name, c.name
"""

# Step 3: Fetch data for selected players
data = pd.read_sql(query, conn, params=players_to_plot)

# Close the connection
conn.close()

# Step 4: Display the data with total goals and assists
print(data[['player_name', 'competition_name', 'total_goals', 'total_assists', 'total_games']])

# Step 5: Plot the data for total goals
plt.figure(figsize=(10, 6))
sns.barplot(x='competition_name', y='total_goals', hue='player_name', data=data)
plt.title('Total Goals by Competition for Selected Players')
plt.xlabel('Competition')
plt.ylabel('Total Goals')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Step 6: Plot the data for total assists
plt.figure(figsize=(10, 6))
sns.barplot(x='competition_name', y='total_assists', hue='player_name', data=data)
plt.title('Total Assists by Competition for Selected Players')
plt.xlabel('Competition')
plt.ylabel('Total Assists')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()