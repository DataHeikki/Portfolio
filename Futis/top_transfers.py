# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 13:37:23 2024

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
         SELECT Players.name, Players.player_id, Transfers.from_club_name, Transfers.to_club_name, Transfers.transfer_fee
         FROM dbo.Players 
         JOIN dbo.Transfers ON Players.player_id = Transfers.player_id
         """)


# Read SQL query into a DataFrame
data = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Preview the DataFrame
print(data)

# Convert transfer_fee to millions of euros
data['transfer_fee'] = data['transfer_fee'] / 1_000_000

# Sort by transfer_fee in descending order and get the top 20
top_20_transfers = data.sort_values(by='transfer_fee', ascending=False).head(20)

# Preview the top 20 transfers
print(top_20_transfers)

plt.figure(figsize=(10,6))
sns.barplot(x='transfer_fee', y='name', data= top_20_transfers, palette='viridis')
plt.title('Top 20 Transfer Fees in M€')
plt.xlabel('Transfer Fee')
plt.ylabel('Player Name')
plt.show()

