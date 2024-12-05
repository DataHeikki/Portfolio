# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:17:30 2024

@author: Heikki
"""

import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Connection to Database
conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost\\SQLEXPRESS;"
    "Database=FootballDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes"
)

# Input season and competition ID before executing query
season = input("Enter the season (e.g., '2022'): ")
competition_id = input("Enter the competition ID: ")  # Treat competition_id as a string

# Query to get data, filtering by season and competition ID
query = f"""
         SELECT cg.club_id, cg.is_win, g.competition_id, g.season, g.home_club_id, g.away_club_id, c.name
         FROM dbo.ClubGames AS cg
         JOIN dbo.Games AS g ON cg.club_id = g.home_club_id OR cg.club_id = g.away_club_id
         JOIN dbo.Clubs AS c ON cg.club_id = c.club_id
         WHERE g.season = '{season}' AND g.competition_id = '{competition_id}'
         """

# Read SQL query into a DataFrame
data = pd.read_sql(query, conn)

# Close the connection
conn.close()

# Print the data to verify it's being fetched correctly
print("Filtered DataFrame:")
print(data.head())

# Calculate points
data['points'] = data['is_win'] * 3
points_summary = data.groupby('name')['points'].sum().reset_index()

# Print the points summary to verify aggregation
print("Points Summary:")
print(points_summary.head())

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

def update(frame):
    ax.clear()
    top_n = points_summary.sort_values('points', ascending=False).head(10)
    if not top_n.empty:
        ax.barh(top_n['name'], top_n['points'], color='skyblue')
        ax.set_xlabel('Points')
        ax.set_title(f'Football Club Points - Season {season}')
        ax.invert_yaxis()
    else:
        ax.text(0.5, 0.5, 'No Data Available', horizontalalignment='center', verticalalignment='center', fontsize=15)

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=range(10), repeat=False)

# Save the animation as a file
ani.save('bar_chart_race.mp4', writer='ffmpeg')

# Show the plot (optional if you want to see a static frame)
plt.show()









