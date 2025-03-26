import kagglehub
import sqlite3
import pandas as pd
#load dataset
path = kagglehub.dataset_download("hugomathien/soccer")
print("Path to dataset files:", path)

database_path = "F:/prometheus/database.sqlite"

#connect to database
conn = sqlite3.connect(database_path)

tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Available tables:", tables)

#show few rows of table country
df = pd.read_sql("SELECT * FROM Country;", conn)
print(df.head())

#describe all tables
def describe_table(table_name):
    query = f"PRAGMA table_info({table_name});"
    columns = pd.read_sql(query, conn)
    print(f"Columns in {table_name}:\n", columns, "\n")

for table in tables['name']:
    describe_table(table)

#show all the foreign keys
for table in tables['name']:
    print(f"Foreign keys in {table}:")
    print(pd.read_sql(f"PRAGMA foreign_key_list({table});", conn), "\n")

df_players = pd.read_sql("SELECT * FROM Player", conn)
df_matches = pd.read_sql("SELECT * FROM Match", conn)
df_teams = pd.read_sql("SELECT * FROM Team", conn)

# Check for missing values
print(df_players.isnull().sum())  
print(df_matches.isnull().sum())  
print(df_teams.isnull().sum())  

# Check for duplicates
print(df_players.duplicated().sum())  
print(df_matches.duplicated().sum())  
print(df_teams.duplicated().sum())

print(df_players.describe())
print(df_matches.describe())
print(df_teams.describe())

#relationship between country and league
leagues = pd.read_sql("""SELECT *
                        FROM League
                        JOIN Country ON Country.id = League.country_id;""", conn)
print(leagues)
