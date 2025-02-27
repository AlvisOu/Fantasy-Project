import httpx, asyncio
from config import YEAR, LEAGUE_ID, SWID, ESPN_S2
import argparse

async def fetch_lineup_data(team_id):
    """
    Fetch the fantasy lineup for a given team ID.
    params: team_id: int
    return: dict {player_id: int: lineup_status: str}
    """

    line_up = {}

    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{YEAR}/segments/0/leagues/{LEAGUE_ID}"

    params = {
        "view": ["mRoster"],
        "leagueId" : LEAGUE_ID,
        "seasonId" : YEAR,
    }

    cookies = {"swid" : SWID, "espn_s2" : ESPN_S2}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, cookies=cookies)
        response.raise_for_status()  # Ensure HTTP errors are raised
        data = response.json()

    for team in data["teams"]:
        if team["id"] != team_id:
            continue
        for player in team["roster"]["entries"]:

            lineup_status = "IR" if player["lineupSlotId"] in [20, 21] else "Starting"

            if player["lineupSlotId"] == 20:
                lineup_status = "Benched"

            # injury_status = player["playerPoolEntry"]["player"].get("injuryStatus", "N/A")
            
            line_up[player["playerId"]] = lineup_status

    return line_up


async def fetch_player_data(player_id):
    """
    Fetch player data from an external API given a player ID.
    params: player_id: int
    return: dict {id: int, name: str, position: str, team: str, projected_score: float, bust_probability: float, boom_probability: float}
    """
    current_year = YEAR
    player = {}
    player_url = f"https://watsonfantasyfootball.espn.com/espnpartner/dallas/players/players_{player_id}_ESPNFantasyFootball_{current_year}.json"
    classifiers_url = f"https://watsonfantasyfootball.espn.com/espnpartner/dallas/classifiers/classifiers_{player_id}_ESPNFantasyFootball_{current_year}.json"

    async with httpx.AsyncClient() as client:

        # using asyncio.gather to make multiple requests concurrently
        player_response, classifier_response = await asyncio.gather(
            client.get(player_url),
            client.get(classifiers_url)
        )

        player_response.raise_for_status()
        classifier_response.raise_for_status()

        player_data = player_response.json()[-1]
        classifier_data = classifier_response.json()[-2:]

    player['id'] = player_id
    player['name'] = player_data['FULL_NAME']
    player['position'] = player_data['POSITION']
    player['team'] = player_data['TEAM']
    player['projected_score'] = player_data['OUTSIDE_PROJECTION']
    player['bust_probability'] = classifier_data[0]['NORMALIZED_RESULT']
    player['boom_probability'] = classifier_data[1]['NORMALIZED_RESULT']

    return player


async def fetch_lineup_and_player(team_id):
    """
    Fetch lineup data and player data concurrently.
    params: team_id: int
    return: tuple (lineup: dict, players: list)
    """
    lineup = await fetch_lineup_data(team_id)
    players = []

    async def helper(player_id):
        player_data = await fetch_player_data(player_id)
        players.append(player_data)

    # using asyncio.gather to make multiple requests concurrently by unpacking * the array of helper coroutines
    await asyncio.gather(*[helper(player_id) for player_id in lineup.keys()])

    return (lineup, players)


async def test_lineup(team_id):
    """Test function to fetch and display lineup data asynchronously."""
    lineup, players = await fetch_lineup_and_player(team_id)
    for id, status in lineup.items():
        print(f"Player ID: {id} - {status}")
    for player in players:
        print(f"Player: {player}")


def main():
    """CLI wrapper for testing."""
    parser = argparse.ArgumentParser(description="Fetch a fantasy lineup for testing.")
    parser.add_argument("team_id", type=int, help="The team ID of the fantasy lineup to fetch.")
    args = parser.parse_args()

    # Run the async function inside an event loop
    asyncio.run(test_lineup(args.team_id))

if __name__ == "__main__":
    main()