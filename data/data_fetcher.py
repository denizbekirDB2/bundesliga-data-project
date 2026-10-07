import requests
import json
from pathlib import Path

# data
#   bl1
#       "season" 2025
#           "matchday" 34...

def fetch_match_day(league, season, match_day):
    response = requests.get(f"https://api.openligadb.de/getmatchdata/{league}/{season}/{match_day}")
    return response.json()

def write_into_json_file(filepath, json_data):
    with open(filepath, "w") as f:
        json.dump(json_data, f)

def fetch_and_write_season(league, season, max_match_days):
    dir = str(Path(__file__).parent.resolve()) + f"/{league}/{season}"
    Path(dir).mkdir(parents=True, exist_ok=True)

    for match_day in range(1, max_match_days + 1):

        json_data = fetch_match_day(league,season,match_day)
        write_into_json_file(dir + f"/{match_day}.json", json_data)

if __name__ == "__main__":
    fetch_and_write_season("bl1", "2024", 34)