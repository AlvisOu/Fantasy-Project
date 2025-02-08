import requests, argparse
from simulation_service.database.models import SessionLocal, PlayerData
from simulation_service.database.db_setup import init_db
from simulation_service.app.utils.lineup_fetcher import fetch_fantasy_lineup

def fetch_external_data(player_id):
    """Fetch player data from an external API given a player ID."""
    current_year = 2024
    player = {}
    player['id'] = player_id

    player_url = f"https://watsonfantasyfootball.espn.com/espnpartner/dallas/players/players_{player_id}_ESPNFantasyFootball_{current_year}.json"
    player_response = requests.get(player_url)
    player_data = player_response.json()[-1]
    player['name'] = player_data['FULL_NAME']
    player['position'] = player_data['POSITION']
    player['team'] = player_data['TEAM']
    player['projected_score'] = player_data['OUTSIDE_PROJECTION']

    classifiers_url = f"https://watsonfantasyfootball.espn.com/espnpartner/dallas/classifiers/classifiers_{player_id}_ESPNFantasyFootball_{current_year}.json"
    classifier_response = requests.get(classifiers_url)
    classifier_data = classifier_response.json()[-2:]
    player['bust_probability'] = classifier_data[0]['NORMALIZED_RESULT']
    player['boom_probability'] = classifier_data[1]['NORMALIZED_RESULT']

    # projections_url = f"https://watsonfantasyfootball.espn.com/espnpartner/dallas/projections/projections_{player_id}_ESPNFantasyFootball_{current_year}.json"
    # projections_response = requests.get(projections_url)

    return player

def seed_database(player_ids):
    """Seed the database with player data."""
    init_db()
    session = SessionLocal()

    for id in player_ids:
        player = fetch_external_data(id)

        player_record = PlayerData(
            id=player['id'],
            player_name=player['name'],
            position=player['position'],
            team=player['team'],
            projected_score=player['projected_score'],
            boom_probability=player['boom_probability'] if player['boom_probability'] is not None else 0.0,
            bust_probability=player['bust_probability'] if player['bust_probability'] is not None else 0.0,
            lineup_status=player_ids[id][0],
            injury_status=player_ids[id][1],
        )

        session.merge(player_record)

    session.commit()
    session.close()
    print("Database seeded with player data!")

def main():
    parser = argparse.ArgumentParser(description='Fetch a fantasy lineup.')
    parser.add_argument('team_id', type=int, help='The team ID of the fantasy lineup to fetch.')
    args = parser.parse_args()
    res = fetch_fantasy_lineup(args.team_id)
    seed_database(res)


if __name__ == "__main__":
    main()
