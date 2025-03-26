import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

database_path = "F:/prometheus/database.sqlite"
conn = sqlite3.connect(database_path)

#player height vs agility
query1 = """
SELECT 
    CASE 
        WHEN ROUND(height) < 165 THEN 165 
        WHEN ROUND(height) > 195 THEN 195 
        ELSE ROUND(height) 
    END AS calc_height, 
    COUNT(height) AS distribution, 
    AVG(pa.agility) AS avg_agility
FROM Player
LEFT JOIN Player_Attributes AS pa ON Player.player_api_id = pa.player_api_id
GROUP BY calc_height
ORDER BY calc_height;
"""
players_height_agility = pd.read_sql(query1, conn)
players_height_agility.dropna(inplace=True)

plt.figure(figsize=(10, 5))

sns.lineplot(x=players_height_agility["calc_height"], y=players_height_agility["avg_agility"], marker="o", color="blue")

plt.xlabel("Player Height (cm)")
plt.ylabel("Average Agility")
plt.title("Player Height vs. Agility")
plt.grid(True)
]
plt.show()

#player height vs jumping
query2 = """
SELECT 
    CASE 
        WHEN ROUND(height) < 165 THEN 165 
        WHEN ROUND(height) > 195 THEN 195 
        ELSE ROUND(height) 
    END AS calc_height, 
    COUNT(height) AS distribution, 
    AVG(pa.jumping) AS avg_jumping
FROM Player
LEFT JOIN Player_Attributes AS pa ON Player.player_api_id = pa.player_api_id
GROUP BY calc_height
ORDER BY calc_height;
"""
players_height_jumping = pd.read_sql(query2, conn)
players_height_jumping.dropna(inplace=True)
plt.figure(figsize=(12, 6))
sns.lineplot(x=players_height_jumping["calc_height"], y=players_height_jumping["avg_jumping"], marker="o", color="blue")

plt.xlabel("Player Height (cm)")
plt.ylabel("Average Jumping Ability")
plt.title("Player Height vs. Jumping Ability")
plt.grid(True)

plt.show()

