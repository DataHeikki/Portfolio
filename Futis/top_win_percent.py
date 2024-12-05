# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 10:47:10 2024

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
         SELECT own_manager_name, is_win
         FROM dbo.ClubGames
         """)

# Read SQL query into a DataFrame
data = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Preview the DataFrame
print("Initial DataFrame:")
print(data.head())

#Calculate total games and wins per manager
manager_stats = data.groupby('own_manager_name').agg(
    total_games=('is_win', 'count'),
    wins=('is_win', 'sum')  # Summing 'is_win' as it is 1 for wins and 0 for losses
).reset_index()

#Filter managers with at least 100 games
manager_stats = manager_stats[manager_stats['total_games'] >= 100]

#Calculate win percentage
manager_stats['win_percentage'] = (manager_stats['wins'] / manager_stats['total_games']) * 100

#Sort by win percentage and get the top 20
top20_managers = manager_stats.sort_values(by='win_percentage', ascending=False).head(20)

#Visualize the top 20 managers with a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x='win_percentage', y='own_manager_name', data=top20_managers, palette='viridis')
plt.title('Top 20 Managers by Win Percentage (Min. 100 Games)')
plt.xlabel('Win Percentage (%)')
plt.ylabel('Manager Name')
plt.show()

# Preview the top 20 managers DataFrame
print(top20_managers)

