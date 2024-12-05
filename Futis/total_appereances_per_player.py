# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 12:21:25 2024

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
         SELECT p.name, p.player_id, p.current_club_name, a.game_id
         FROM dbo.Players AS p
         JOIN dbo.Appereances AS a ON p.player_id = a.player_id
         """)

# Read SQL query into a DataFrame
data = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Preview the DataFrame
print(data.head())

# Calculate the number of appearances per player
appearance_counts = data.groupby('name')['game_id'].count().reset_index()
appearance_counts.columns = ['name', 'total_appearances']

# Sort by total appearances in descending order
top_appearances = appearance_counts.sort_values(by='total_appearances', ascending=False)

# Preview the top appearances
print(top_appearances.head(20))

# Plot the top 20 players by number of appearances
plt.figure(figsize=(12, 10))
sns.barplot(x='total_appearances', y='name', data=top_appearances.head(20), palette='viridis')
plt.title('Top 20 Players by Number of Appearances')
plt.xlabel('Total Appearances')
plt.ylabel('Player Name')

# Rotate y-axis labels if needed
plt.yticks(rotation=0)

# Adjust layout to fit all labels
plt.tight_layout()

plt.show()
