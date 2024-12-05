# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 13:11:57 2024

@author: Heikki
"""

import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# List of teams to filter
teams_to_filter = ['PSV Eindhoven']  # Replace with actual team names

# Create a comma-separated list of team names for the SQL query
teams_placeholder = ', '.join(f"'{team}'" for team in teams_to_filter)

# Connection to Database
conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost\\SQLEXPRESS;"
    "Database=FootballDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes"
)

# Query to get data filtered by specific teams
query = (f"""
         SELECT c.club_id, c.name, g.away_club_id, g.home_club_id, g.home_club_formation, g.away_club_formation,
                cg.club_id AS game_club_id, cg.is_win
         FROM dbo.Clubs AS c
         JOIN dbo.Games AS g 
         ON c.club_id = g.home_club_id  
         OR c.club_id = g.away_club_id  
         JOIN dbo.ClubGames AS cg 
         ON c.club_id = cg.club_id
         WHERE c.name IN ({teams_placeholder})
         """)

# Read SQL query into a DataFrame
data = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Preview the DataFrame
print("Initial DataFrame:")
print(data.head())

# Replace 'unknown' with NaN for easier filtering
data.replace('unknown', pd.NA, inplace=True)

# Drop rows where any of the relevant columns are NaN
data = data.dropna(subset=['home_club_formation', 'away_club_formation', 'is_win'])

# Separate home and away formations
home_data = data[['club_id', 'name', 'home_club_formation', 'is_win']]
home_data = home_data.rename(columns={'home_club_formation': 'formation', 'is_win': 'win'})

away_data = data[['club_id', 'name', 'away_club_formation', 'is_win']]
away_data = away_data.rename(columns={'away_club_formation': 'formation', 'is_win': 'win'})

# Combine home and away data
combined_data = pd.concat([home_data, away_data], ignore_index=True)

# Drop rows where formation is 'unknown'
combined_data = combined_data[combined_data['formation'] != 'unknown']

# Print combined data for debugging
print("Combined Data:")
print(combined_data.head())

# Count the number of games and wins for each formation
formation_stats = combined_data.groupby('formation').agg(
    total_games=('win', 'size'),
    total_wins=('win', 'sum')
).reset_index()

# Calculate win rate
formation_stats['win_rate'] = (formation_stats['total_wins'] / formation_stats['total_games']) * 100

# Print formation stats for debugging
print("Formation Stats:")
print(formation_stats.head())

# Sort formations by win rate and total games
formation_stats = formation_stats.sort_values(by=['win_rate', 'total_games'], ascending=[False, False])

# Plotting the win rate for the top formations
plt.figure(figsize=(14, 8))
sns.barplot(data=formation_stats, x='win_rate', y='formation', palette='Blues_d')

plt.title('Win Rate of Formations')
plt.xlabel('Win Rate (%)')
plt.ylabel('Formation')
plt.tight_layout()

plt.show()




