import pandas as pd
import sqlite3

df = pd.read_csv("ipl_players_dataset.csv")

df.insert(0, "id", range(1, len(df)+1))

conn = sqlite3.connect("players.db")

df.to_sql("players", conn, if_exists="replace", index=False)

conn.close()

print("Database created successfully")