# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 11:52:32 2024

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
         SELECT p.name, p.player_id, p.current_club_name, a.assists
         FROM dbo.Players AS p
         JOIN dbo.Appereances AS a ON p.player_id = a.player_id
         """)

# Read SQL query into a DataFrame
data = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Preview the DataFrame
print(data)

# Calculate total assists by player
total_assists = data.groupby('name')['assists'].sum().reset_index()

# Sort by total assists in descending order
top_assisters = total_assists.sort_values(by='assists', ascending=False)

# Preview the top assisters
print(top_assisters)

# Plot the top 20 assisters
plt.figure(figsize=(12, 10))
sns.barplot(x='assists', y='name', data=top_assisters.head(20), palette='viridis')
plt.title('Top 20 Assisters')
plt.xlabel('Total Assists')
plt.ylabel('Player Name')

# Rotate y-axis labels if needed
plt.yticks(rotation=0)

# Adjust layout to fit all labels
plt.tight_layout()

plt.show()

