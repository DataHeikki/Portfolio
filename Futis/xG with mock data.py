# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:15:45 2024

@author: Heikki
"""

import pandas as pd
import numpy as np

# Sample dataset
data = {
    'shot_id': [1, 2, 3, 4],
    'player_name': ['Player 1', 'Player 2', 'Player 3', 'Player 4'],
    'team': ['Team A', 'Team A', 'Team B', 'Team B'],
    'x': [12, 18, 10, 5],  # Distance from goal
    'y': [15, 30, 5, 10],  # Y-coordinate
    'angle': [30, 45, 20, 10],  # Angle in degrees
    'shot_type': ['foot', 'header', 'foot', 'foot'],
    'is_goal': [0, 1, 0, 1],
}

df = pd.DataFrame(data)

# Simplified xG model based on distance and angle (assumed probabilities)
def calculate_xg(distance, angle, shot_type):
    if shot_type == 'header':
        return max(0.05, 0.15 - 0.01 * distance + 0.01 * np.cos(np.radians(angle)))
    else:
        return max(0.05, 0.2 - 0.01 * distance + 0.02 * np.cos(np.radians(angle)))

# Apply the function to each row
df['xG'] = df.apply(lambda row: calculate_xg(row['x'], row['angle'], row['shot_type']), axis=1)

# Total xG for the match (sum of xG values)
df['xG_total'] = df.groupby('team')['xG'].transform('sum')

print(df)
