from fastapi import APIRouter, Depends
from utils.redis_cache import store_player, player_exists, get_player
from utils.lineup_fetcher import fetch_player_data
from dependencies import get_redis

router = APIRouter()

@router.get("/{player_id}")
async def get_player_data(player_id: int, redis=Depends(get_redis)):
    """Get the player data."""
    
    # If the player data is already stored in Redis, retrieve it
    if await player_exists(redis, player_id):
        player_data = await get_player(redis, player_id)

    # Otherwise, fetch the player data
    else:
        player_data = await fetch_player_data(player_id)
        await store_player(redis, player_id, player_data)
    
    return player_data

@router.put("/{player_id}")
async def update_player_data(player_id: int, redis=Depends(get_redis)):
    """Update the player data."""
    
    # Fetch the updated player data
    player_data = await fetch_player_data(player_id)
    
    # Store the updated player data in Redis
    await store_player(redis, player_id, player_data)
    
    return player_data