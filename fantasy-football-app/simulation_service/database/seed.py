import requests, argparse
from simulation_service.database.models import SessionLocal, PlayerData
from simulation_service.database.db_setup import init_db
# from simulation_service.app.utils.lineup_fetcher import fetch_fantasy_lineup

def fetch_external_data(player_id):
    """Fetch player data from an external API given a player ID."""
    current_year = 2024
    tuesdays = {} # date to week number

    data = []

    player_url = f"https://watsonfantasyfootball.espn.com/espnpartner/dallas/players/players_{player_id}_ESPNFantasyFootball_{current_year}.json"
    player_response = requests.get(player_url)
    player_data = player_response.json()

    classifiers_url = f"https://watsonfantasyfootball.espn.com/espnpartner/dallas/classifiers/classifiers_{player_id}_ESPNFantasyFootball_{current_year}.json"
    classifier_response = requests.get(classifiers_url)
    classifier_data = classifier_response.json()

    for entry in player_data:
        player = {}
        player['player_id'] = player_id
        player['name'] = entry['FULL_NAME']
        player['position'] = entry['POSITION']
        player['team'] = entry['TEAM']
        player['projected_score'] = entry['OUTSIDE_PROJECTION']
        data.append(player)

    for entry in classifier_data:
        if entry['DATA_TIMESTAMP'] in tuesdays:
            player = data[tuesdays[entry['DATA_TIMESTAMP']]]
            if entry['MODEL_TYPE'] == 'bust_classifier':
                player['bust_probability'] = entry['NORMALIZED_RESULT']
            elif entry['MODEL_TYPE'] == 'boom_classifier':
                player['boom_probability'] = entry['NORMALIZED_RESULT']

    # Need an api to get actual points, injury status, and, if possible, what fantasy team they were on and lineup status
            
    return data

def seed_database(player_ids):
    """
    Seed the database with player data.
    """
    init_db()
    session = SessionLocal()

    for id in player_ids:
        player = fetch_external_data(id)

        for i in range(len(player)):
            
            player_record = PlayerData(
                player_id=player['player_id'],
                week = i + 1,
                player_name=player['name'],
                position=player['position'],
                team=player['team'],
                projected_score=player['projected_score'],
                boom_probability=player['boom_probability'] if player['boom_probability'] is not None else 0.0,
                bust_probability=player['bust_probability'] if player['bust_probability'] is not None else 0.0,
                actual_score=player['actual_score'] if player['actual_score'] is not None else 0.0,
                injury_status=player['injury_status'] if player['injury_status'] is not None else "N/A",
                lineup_status=player['lineup_status'] if player['lineup_status'] is not None else "N/A",
                fantasy_team=player['fantasy_team'] if player['fantasy_team'] is not None else "N/A",
            )
            session.add(player_record)

    session.commit()
    session.close()
    print("Database seeded with player data!")

def main():
    ids = []
    seed_database(ids)


if __name__ == "__main__":
    main()
