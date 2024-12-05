# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 11:25:01 2024

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
         SELECT stadium, attendance
         FROM dbo.Games
         """)

# Read SQL query into a DataFrame
data = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Preview the DataFrame
print(data.head())

# Group by stadium and calculate the average attendance
stadium_avg_attendance = data.groupby('stadium')['attendance'].mean().reset_index()

# Sort by average attendance in descending order and select the top 20 stadiums
top_20_stadiums = stadium_avg_attendance.sort_values(by='attendance', ascending=False).head(20)

# Preview the top 20 stadiums with their average attendance
print(top_20_stadiums)

# Visualization using seaborn
plt.figure(figsize=(14, 8))
sns.barplot(data=top_20_stadiums, x='attendance', y='stadium', palette='Blues_d')

plt.title('Top 20 Stadiums by Average Attendance')
plt.xlabel('Average Attendance')
plt.ylabel('Stadium')
plt.tight_layout()

plt.show()
