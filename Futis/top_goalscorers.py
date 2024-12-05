# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 12:17:59 2024

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
         SELECT p.name, p.player_id, p.current_club_name, a.goals
         FROM dbo.Players AS p
         JOIN dbo.Appereances AS a ON p.player_id = a.player_id
         """)

# Read SQL query into a DataFrame
data = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Preview the DataFrame
print(data)

# Calculate total goals by player
total_goals = data.groupby('name')['goals'].sum().reset_index()

# Sort by total goals in descending order
top_goalscorers = total_goals.sort_values(by='goals', ascending=False)

# Preview the top goalscorers
print(top_goalscorers)

# Plot the top 20 goalscorers
plt.figure(figsize=(12, 10))
sns.barplot(x='goals', y='name', data=top_goalscorers.head(20), palette='viridis')
plt.title('Top 20 goalscorers')
plt.xlabel('Total Goals')
plt.ylabel('Player Name')

# Rotate y-axis labels if needed
plt.yticks(rotation=0)

# Adjust layout to fit all labels
plt.tight_layout()

plt.show()