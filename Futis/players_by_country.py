# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 13:01:52 2024

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
query = "SELECT [country_of_citizenship] FROM dbo.players;"
data = pd.read_sql(query, conn)

# Get value counts of agent names
country_counts = data['country_of_citizenship'].value_counts().reset_index()
country_counts.columns = ['country_of_citizenship', 'count']

top_countries = country_counts.head(20)

print(top_countries)

# Horizontal Bar Plot
plt.figure(figsize=(14, 10))  # Further increase the figure size for better readability
sns.barplot(y='country_of_citizenship', x='count', data=top_countries, palette="viridis")  # Horizontal bar plot
plt.xlabel('Number of Countries')
plt.ylabel('Country Name')
plt.title('Top 20 Countries by Number of Players')
plt.tight_layout()  # Adjust layout to prevent clipping
plt.show()