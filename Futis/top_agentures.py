# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 12:05:59 2024

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
cursor = conn.cursor()

# Query to get agent names
query = "SELECT [agent_name] FROM dbo.players;"
data = pd.read_sql(query, conn)

# Get value counts of agent names
agent_counts = data['agent_name'].value_counts().reset_index()
agent_counts.columns = ['agent_name', 'count']

# Optionally, limit to top 20 agents for clarity
top_agents = agent_counts.head(20)

# Check the data
print(top_agents)

# Horizontal Bar Plot
plt.figure(figsize=(14, 10))  # Further increase the figure size for better readability
sns.barplot(y='agent_name', x='count', data=top_agents, palette="viridis")  # Horizontal bar plot
plt.xlabel('Number of Players')
plt.ylabel('Agent Name')
plt.title('Top 20 Agents by Number of Players')
plt.tight_layout()  # Adjust layout to prevent clipping
plt.show()
