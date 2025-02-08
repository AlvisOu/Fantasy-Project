import json
from redis import asyncio as aioredis
from fastapi import Depends

# Redis connection settings
REDIS_HOST = "localhost"
REDIS_PORT = 6379

# Dependency for Redis client
async def get_redis_client():
    redis = await aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)
    try:
        yield redis
    finally:
        await redis.close()

async def cache_player_data(redis, player_id: int, player_data: dict, expiration: int = 3600):
    """
    Cache player data in Redis with an expiration time.

    Args:
        redis (aioredis.Redis): The Redis client.
        player_id (int): The ID of the player.
        player_data (dict): The player data to cache.
        expiration (int): Expiration time in seconds (default: 1 hour).
    """
    try:
        await redis.set(f"player:{player_id}", json.dumps(player_data), ex=expiration)
    except Exception as e:
        print(f"Error caching data for player {player_id}: {e}")

async def get_cached_player_data(redis, player_id: int):
    """
    Retrieve player data from Redis.

    Args:
        redis (aioredis.Redis): The Redis client.
        player_id (int): The ID of the player.

    Returns:
        dict or None: The cached player data or None if not found.
    """
    try:
        cached_data = await redis.get(f"player:{player_id}")
        if cached_data:
            return json.loads(cached_data)
    except Exception as e:
        print(f"Error retrieving data for player {player_id}: {e}")
    return None
