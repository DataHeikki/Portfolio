# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 11:37:35 2024

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

# Query to get wanted data
query = ("""
         SELECT Players.name, Players.player_id, PlayerValuations.market_value_in_eur
         FROM dbo.Players 
         JOIN dbo.PlayerValuations ON Players.player_id = PlayerValuations.player_id
         """)

# Read SQL query into a DataFrame
data = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Convert market_value_in_eur to millions of euros
data['market_value_in_eur'] = data['market_value_in_eur'] / 1_000_000

# Remove duplicates, keeping the entry with the highest market value
data = data.sort_values(by='market_value_in_eur', ascending=False).drop_duplicates(subset='name', keep='first')

# Sort by market_value_in_eur in descending order and get the top 20
top_20_values = data.sort_values(by='market_value_in_eur', ascending=False).head(20)

# Check the data to ensure it's correct
print(top_20_values.shape)  
print(top_20_values.head(20))  

# Plot the top 20 player values
plt.figure(figsize=(16, 20))  
sns.barplot(x='market_value_in_eur', y='name', data=top_20_values, palette='viridis')
plt.title('Top 20 Player Values in M€')
plt.xlabel('Market Value (Millions of Euros)')
plt.ylabel('Player Name')

# Rotate y-axis labels 
plt.yticks(rotation=0)

# Adjust layout to fit all labels
plt.tight_layout()

plt.show()
