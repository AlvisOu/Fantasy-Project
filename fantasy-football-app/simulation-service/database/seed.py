import requests
from models import SessionLocal, PlayerData
from db_setup import init_db

team_hashmap = {
    '8': "Detroit Lions",
}

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

        existing_player = session.query(PlayerData).filter_by(id=player['id']).first()

        if existing_player:
            existing_player['projected_score'] = player['projected_score']
            existing_player['boom_probability'] = player['boom_probability']
            existing_player['bust_probability'] = player['bust_probability']
            print(f"Updated player data for {player['name']}")

        else:
            new_player = PlayerData(
                id=player['id'],
                player_name=player['name'],
                position=player['position'],
                team=player['team'],
                projected_score=player['projected_score'],
                boom_probability=player['boom_probability'],
                bust_probability=player['bust_probability']
            )
            session.add(new_player)
            print(f"Added player data for {player['name']}")

    session.commit()
    session.close()
    print("Database seeded with player data!")

if __name__ == "__main__":
    seed_database()
