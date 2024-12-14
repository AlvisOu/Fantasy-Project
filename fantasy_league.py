import requests
import pandas as pd
import json

YEAR = 2024
LEAGUE_ID = "432959547"
ESPN_S2 = 'AEAGstGzfVapLBUQjvAdZ6GzYXnNn%2F6zaJ1aKBaGfodSbZlAvSQCksL5cBPrQ2nvyg5B72c8fSTcMW1iUMMvVr9l9xF0WsaJz%2Fikact6HAV52u1AfskuMr1N9%2FxfssqkMhkJtnXMp3RxvVqMqvYI9GG%2FnpJBt7rTy%2BojPYRqFzOiodrozlh9%2F%2FwVppny6vLdnZMgV2RrJCbA4cGGTIWXHZJhMFFCuyrMGp6z3zoTAlGtif%2FRZCeD2gs4HQXBGPKtqzBPBeyBgiG1BJsBGmPUuv4PRKsEQibW%2Fs1ka3jCHfRUg87NAu%2B%2F6xJI1k7jX3VjVYU%3D'
SWID = '{534A91A4-961E-4087-BE49-51DCDD461E9C}'

# Function to fetch paginated player data
def fetch_players(limit=300):

    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{YEAR}/segments/0/leagues/{LEAGUE_ID}"

    filters = {
        "players": {
            
            "limit": limit,
            "sortAppliedStatTotal": {
                "sortAsc": False, 
                "sortPriority": 1,
                "value": f"00{YEAR}"
            }
        }
    }

    headers = {
        'X-Fantasy-Filter': json.dumps(filters)
    }

    params = {
        "league": LEAGUE_ID,
        "seasonId": YEAR,
        "view": "kona_player_info",
    }

    cookies={"swid" : SWID, "espn_s2" : ESPN_S2}

    response = requests.get(url, params=params, cookies=cookies, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return []

    players_data = response.json()['players']
    return players_data


# Fetch and process player data
def process_players(players_data, position):
    player_list = []
    for player in players_data:

        if player["player"]["defaultPositionId"] != position:
            continue

        stats = player['player']["stats"]
        for stat in stats:
            if stat.get("id") == "002024":
                player_list.append({
                    "name": player["player"]["fullName"],
                    "position": player["player"]["defaultPositionId"],
                    "team": player["player"]["proTeamId"],
                    "points": stat.get("appliedTotal", 0)  # Total fantasy points
                })

    return player_list

# Main script
if __name__ == "__main__":

    positions = {
        1: "QB",
        2: "RB",
        3: "WR",
        4: "TE",
    }

    players_data = fetch_players()  # Fetch all player data

    if not players_data:
        print("No data fetched")
        exit()

    for position in positions:
        player_list = process_players(players_data, position)

        # Create DataFrame and sort by points
        df = pd.DataFrame(player_list)

        # Save to CSV
        output_file = f"top_{positions[position]}s.csv"
        df.to_csv(output_file, index=True)
        print(f"Top_{positions[position]}s saved to {output_file}")
