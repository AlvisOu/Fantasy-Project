import json

async def store_player(redis, player_id: str, player_data: dict):
    """Stores a player's data in Redis with a TTL (time-to-live)."""
    # redis only stores strings, so we need to serialize the data into a JSON string
    await redis.set(f"player:{player_id}", json.dumps(player_data), ex=86400)  # Expire in 24 hours

async def get_player(redis, player_id: str):
    """Retrieves a player's data from Redis, returns None if not found."""
    data = await redis.get(f"player:{player_id}")
    return json.loads(data) if data else None

async def player_exists(redis, player_id: str):
    """Checks if a player's data is in Redis."""
    return await redis.exists(f"player:{player_id}")

async def store_lineup(redis, team_id: str, lineup_data: dict):
    """Stores a team's lineup in Redis."""
    await redis.set(f"lineup:{team_id}", json.dumps(lineup_data), ex=86400)  # Expire in 24 hours

async def get_lineup(redis, team_id: str):
    """Retrieves a team's lineup from Redis."""
    data = await redis.get(f"lineup:{team_id}")
    return json.loads(data) if data else None
