import json
import os
from pathlib import Path
from pprint import pprint

def count_files(league, season):
    path = str(Path(__file__).parent.parent) + f"/data/{league}/{season}"
    files = os.listdir(path)

    num_files = sum(1 for f in files if os.path.isfile(os.path.join(path, f)))
    print(num_files)

def get_files(league, season):
    path = str(Path(__file__).parent.parent) + f"/data/{league}/{season}"
    files = os.listdir(path)

    return files

def read_json_file(filepath):
    with open(filepath) as f:
        json_data = json.load(f)
        return json_data

def get_match_day(league, season, match_day):
    path = str(Path(__file__).parent.parent) + f"/data/{league}/{season}/{match_day}.json"
    return read_json_file(path)

# (teamId, teamName)
def get_all_teams(match_day_json):
    all_teams = []
    for match in match_day_json:
        team1 = (match["team1"]["teamId"],match["team1"]["teamName"])
        team2 = (match["team2"]["teamId"],match["team2"]["teamName"])

        all_teams.append(team1)
        all_teams.append(team2)

    return sorted(
        all_teams, key=lambda x: x[1]
    )

def points_and_goals(match_day_json):
    points = {}
    goals = {}

    for match in match_day_json:
        endresult = match["matchResults"][1]
        if endresult["pointsTeam1"] > endresult["pointsTeam2"]: # team1 win
            points[match["team1"]["teamId"]] = 3
            points[match["team2"]["teamId"]] = 0
        elif endresult["pointsTeam1"] < endresult["pointsTeam2"]: # team2 win
            points[match["team1"]["teamId"]] = 0
            points[match["team2"]["teamId"]] = 3
        else:
            points[match["team1"]["teamId"]] = 1
            points[match["team2"]["teamId"]] = 1

        goals[match["team1"]["teamId"]] = endresult["pointsTeam1"]
        goals[match["team2"]["teamId"]] = endresult["pointsTeam2"]

    return points, goals

def table_match_day_x(league, season, match_days):
    table = {}
    all_teams = get_all_teams(get_match_day(league, season, 1))
    for team in all_teams:
        table[team[0]] = {"points":0,"goals":0}

    for match_day in range(1, match_days + 1):
        match_day_json = get_match_day(league, season, match_day)
        points, goals = points_and_goals(match_day_json)

        for keys, values in points.items():
            table[keys]["points"] = table[keys]["points"] + values


        for keys, values in goals.items():
            table[keys]["goals"] = table[keys]["goals"] + values

    return table

#todo W/D/L G/GA/GD Points

if __name__ == "__main__":
    league = "bl1"
    season = "2025"

    table_match_day_x(league,season,34)