# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:52:24 2024

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

# Step 4: Calculate goals/assists per game
data['goals_per_game'] = data['total_goals'] / data['total_games']
data['assists_per_game'] = data['total_assists'] / data['total_games']

# Display the updated data with calculations
print(data[['player_name', 'competition_name', 'total_goals', 'total_assists', 'total_games', 'goals_per_game', 'assists_per_game']])

# Step 5: Plot the data for goals per game
plt.figure(figsize=(10, 6))
sns.barplot(x='competition_name', y='goals_per_game', hue='player_name', data=data)
plt.title('Goals Per Game by Competition for Selected Players')
plt.xlabel('Competition')
plt.ylabel('Goals Per Game')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Step 6: Plot the data for assists per game
plt.figure(figsize=(10, 6))
sns.barplot(x='competition_name', y='assists_per_game', hue='player_name', data=data)
plt.title('Assists Per Game by Competition for Selected Players')
plt.xlabel('Competition')
plt.ylabel('Assists Per Game')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


