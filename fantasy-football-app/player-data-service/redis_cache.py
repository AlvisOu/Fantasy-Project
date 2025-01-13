import redis
import json

# Connect to Redis
REDIS_HOST = "localhost"
REDIS_PORT = 6379
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def cache_player_data(player_id, player_data, expiration=3600):
    """
    Cache player data in Redis with an expiration time.
    
    Args:
        player_id (int): The ID of the player.
        player_data (dict): The player data to cache.
        expiration (int): Expiration time in seconds (default: 1 hour).
    """
    redis_client.set(f"player:{player_id}", json.dumps(player_data), ex=expiration)

def get_cached_player_data(player_id):
    """
    Retrieve player data from Redis.
    
    Args:
        player_id (int): The ID of the player.
    
    Returns:
        dict or None: The cached player data or None if not found.
    """
    cached_data = redis_client.get(f"player:{player_id}")
    if cached_data:
        return json.loads(cached_data)
    return None

if __name__ == "__main__":
    # Example usage
    player_id = 1
    player_data = {
        "player_name": "Patrick Mahomes",
        "position": "QB",
        "team": "Chiefs",
        "projected_score": 25.3,
        "boom_probability": 0.4,
        "bust_probability": 0.1
    }

    # Cache the player data
    cache_player_data(player_id, player_data)
    print("Player data cached!")

    # Retrieve the player data
    retrieved_data = get_cached_player_data(player_id)
    print("Retrieved from cache:", retrieved_data)
