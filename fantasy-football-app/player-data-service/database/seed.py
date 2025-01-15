import requests
from models import SessionLocal, PlayerData
from db_setup import init_db

def fetch_external_data(player_id):
    """Fetch player data from an external API given a player ID."""
    current_year = 2024
    classifiers_url = f"https://watsonfantasyfootball.espn.com/espnpartner/dallas/classifiers/classifiers_{player_id}_ESPNFantasyFootball_{current_year}.json"
    classifier_response = requests.get(classifiers_url)
    projections_url = f"https://watsonfantasyfootball.espn.com/espnpartner/dallas/projections/projections_{player_id}_ESPNFantasyFootball_{current_year}.json"
    projections_response = requests.get(projections_url)

    # TODO: Parse the JSON responses and extract relevant data before returning

def seed_data():
    """Seed the database with player data."""
    init_db()
    session = SessionLocal()

    player_data = fetch_external_data()
    for player in player_data:
        new_player = PlayerData(
            player_name=player['name'],
            position=player['position'],
            team=player['team'],
            projected_score=player['projected_score'],
            boom_probability=player['boom_probability'],
            bust_probability=player['bust_probability']
        )
        session.add(new_player)

    session.commit()
    session.close()
    print("Database seeded with player data!")

if __name__ == "__main__":
    seed_data()
