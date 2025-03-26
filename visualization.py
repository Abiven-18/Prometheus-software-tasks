import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#visualize home advantage
query = """
WITH HomeWins AS (
    SELECT 
        League.name AS league_name,
        COUNT(*) AS home_wins
    FROM Match
    JOIN League ON Match.league_id = League.id
    JOIN Country ON Country.id = League.country_id
    WHERE Match.home_team_goal > Match.away_team_goal
    AND Country.name IN ('Spain', 'England', 'France', 'Germany', 'Italy')
    AND Match.season = '2015/2016'
    GROUP BY League.name
),
AwayWins AS (
    SELECT 
        League.name AS league_name,
        COUNT(*) AS away_wins
    FROM Match
    JOIN League ON Match.league_id = League.id
    JOIN Country ON Country.id = League.country_id
    WHERE Match.away_team_goal > Match.home_team_goal
    AND Country.name IN ('Spain', 'England', 'France', 'Germany', 'Italy')
    AND Match.season = '2015/2016'
    GROUP BY League.name
)
SELECT 
    HomeWins.league_name, 
    HomeWins.home_wins, 
    AwayWins.away_wins
FROM HomeWins
JOIN AwayWins ON HomeWins.league_name = AwayWins.league_name
ORDER BY HomeWins.league_name;
"""
df = pd.read_sql(query, conn)
df_melted = df.melt(id_vars=["league_name"], value_vars=["home_wins", "away_wins"], var_name="Win Type", value_name="Wins")

plt.figure(figsize=(12, 6))
sns.barplot(x="league_name", y="Wins", hue="Win Type", data=df_melted, palette=["blue", "red"])

plt.xlabel("League")
plt.ylabel("Number of Wins")
plt.title("Home Wins vs Away Wins (2015/2016 Season)")
plt.legend(title="Win Type", labels=["Home Wins", "Away Wins"])

plt.show()

#avg goals per match
df_team_perf = pd.read_sql("""SELECT season, home_team_api_id, home_team_goal, away_team_goal FROM Match""", conn)
df_team_perf["total_goals"] = df_team_perf["home_team_goal"] + df_team_perf["away_team_goal"]
df_season_perf = df_team_perf.groupby("season")["total_goals"].mean().reset_index()

sns.lineplot(x=df_season_perf["season"], y=df_season_perf["total_goals"], marker="o")
plt.xticks(rotation=45)
plt.title("Average Goals Per Match Over Seasons")
plt.xlabel("Season")
plt.ylabel("Average Goals per Match")
plt.show()

#home vs away wins in england each seasons 
detailed_matches = pd.read_sql("""SELECT season, 
                                        home_team_goal, 
                                        away_team_goal
                                FROM Match
                                JOIN Country on Country.id = Match.country_id
                                WHERE Country.name = 'England'
                                ORDER by season;""", conn)
detailed_matches["home_win"] = detailed_matches["home_team_goal"] > detailed_matches["away_team_goal"]
detailed_matches["away_win"] = detailed_matches["away_team_goal"] > detailed_matches["home_team_goal"]

seasonal_wins = detailed_matches.groupby("season").agg({"home_win": "sum", "away_win": "sum"}).reset_index()

plt.figure(figsize=(12, 6))
sns.lineplot(data=seasonal_wins, x="season", y="home_win", label="Home Wins", marker="o")
sns.lineplot(data=seasonal_wins, x="season", y="away_win", label="Away Wins", marker="s")

plt.title("Home vs Away Wins Over Seasons (England)")
plt.xlabel("Season")
plt.ylabel("Number of Wins")
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.show()


