import json
import os
from pathlib import Path
from pprint import pprint

#W/D/L G/GA/GD Points
class Team():

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.wins = 0
        self.draws = 0
        self.defeats = 0
        self.goals = 0
        self.goals_against = 0
        self.goal_difference = 0
        self.points = 0

    def update(self):
        self.goal_difference = self.goals - self.goals_against
        self.points = self.wins * 3 + self.draws

    def add_win(self):
        self.wins += 1

    def add_draw(self):
        self.draws += 1

    def add_defeat(self):
        self.defeats += 1

    def add_goals(self, goals):
        self.goals += goals

    def add_goals_against(self, goals_against):
        self.goals_against += goals_against

    def __str__(self):
        result = f"| {self.name:<26} | {self.wins:>2} | {self.draws:>2} | {self.defeats:>2} | {self.goals:>3} | {self.goals_against:>3} | {self.goal_difference:>3} | {self.points:>3} |"
        return result

def read_json_file(filepath):
    with open(filepath) as f:
        json_data = json.load(f)
        return json_data

def get_match_day(league, season, match_day):
    path = str(Path(__file__).parent.parent) + f"/data/{league}/{season}/{match_day}.json"
    return read_json_file(path)

def init_teams(match_day_json):
    teams = {}
    for match in match_day_json:
        teams[match["team1"]["teamId"]] = (Team(match["team1"]["teamName"], match["team1"]["teamId"]))
        teams[match["team2"]["teamId"]] = (Team(match["team2"]["teamName"], match["team2"]["teamId"]))

    return teams

def set_result(match_day_json, teams):

    for match in match_day_json:
        endresult = match["matchResults"][1]
        team1Id = match["team1"]["teamId"]
        team2Id = match["team2"]["teamId"]

        teams[team1Id].add_goals(endresult["pointsTeam1"])
        teams[team1Id].add_goals_against(endresult["pointsTeam2"])

        teams[team2Id].add_goals(endresult["pointsTeam2"])
        teams[team2Id].add_goals_against(endresult["pointsTeam1"])

        if endresult["pointsTeam1"] > endresult["pointsTeam2"]: # team1 win
            teams[team1Id].add_win()
            teams[team2Id].add_defeat()

        elif endresult["pointsTeam1"] < endresult["pointsTeam2"]: # team2 win
            teams[team1Id].add_defeat()
            teams[team2Id].add_win()  
        else:
            teams[team1Id].add_draw()
            teams[team2Id].add_draw()

    return teams

def table_of_matchday(league, season, match_day):
    teams = init_teams(get_match_day(league, season, match_day))

    for day in range(1,match_day+1):
        match_day_json = get_match_day(league, season, day)
        set_result(match_day_json, teams)

    for value in teams.values():
        value.update()

    sorted_teams = {k: v for k,v in sorted(teams.items(), key = lambda item: (item[1].points, item[1].goal_difference, item[1].goals), reverse=True)}

    return sorted_teams

def print_table(table):
    for value, i in zip(table.values(),range(1, len(table)+1)):
        print(f"{str(i) + ".":<3} {value}")

if __name__ == "__main__":
    league = "bl1"
    season = "2025"

    print_table(table_of_matchday(league, season, 34))
