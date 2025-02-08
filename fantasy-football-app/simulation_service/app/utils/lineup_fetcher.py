import requests
import argparse

LEAGUE_ID = "432959547"
YEAR = 2024
ESPN_S2 = 'AEAGstGzfVapLBUQjvAdZ6GzYXnNn%2F6zaJ1aKBaGfodSbZlAvSQCksL5cBPrQ2nvyg5B72c8fSTcMW1iUMMvVr9l9xF0WsaJz%2Fikact6HAV52u1AfskuMr1N9%2FxfssqkMhkJtnXMp3RxvVqMqvYI9GG%2FnpJBt7rTy%2BojPYRqFzOiodrozlh9%2F%2FwVppny6vLdnZMgV2RrJCbA4cGGTIWXHZJhMFFCuyrMGp6z3zoTAlGtif%2FRZCeD2gs4HQXBGPKtqzBPBeyBgiG1BJsBGmPUuv4PRKsEQibW%2Fs1ka3jCHfRUg87NAu%2B%2F6xJI1k7jX3VjVYU%3D'
SWID = '{534A91A4-961E-4087-BE49-51DCDD461E9C}'

def fetch_fantasy_lineup(team_id):

    line_up = {}

    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{YEAR}/segments/0/leagues/{LEAGUE_ID}"

    # Without scoringPeriodId, it defualts to the current week's lineup
    params = {
        "view": ["mRoster"],
        "leagueId" : LEAGUE_ID,
        "seasonId" : YEAR,
        # "scoringPeriodId": 18
    }

    response = requests.get(url, 
                        params=params,
                        # headers=headers,
                        cookies={"swid" : SWID,
                                "espn_s2" : ESPN_S2},)

    json = response.json()
    for team in json["teams"]:
        if team["id"] != team_id:
            continue
        for player in team["roster"]["entries"]:
            lineup_status = "IR"
            injury_status = player["playerPoolEntry"]["player"].get("injuryStatus", "N/A")
            if player["lineupSlotId"] not in [20, 21]:
                lineup_status = "Starting"
                # print(f"Started {player["playerPoolEntry"]["player"]["fullName"]}.")

            elif player["lineupSlotId"] == 20:
                lineup_status = "Benched"
                # print(f"Benched {player["playerPoolEntry"]["player"]["fullName"]}.")

            # else:
            #     print(f"Had {player["playerPoolEntry"]["player"]["fullName"]} on IR.")
            
            line_up[player["playerId"]] = (lineup_status, injury_status)
        # print("\n")

    return line_up

def main():
    parser = argparse.ArgumentParser(description='Fetch a fantasy lineup.')
    parser.add_argument('team_id', type=int, help='The team ID of the fantasy lineup to fetch.')
    args = parser.parse_args()

    res = fetch_fantasy_lineup(args.team_id)
    # for player, status in res.items():
    #     print(f"Player ID: {player}, Status: {status}")


if __name__ == "__main__":
    main()