import asyncio
from fastapi import APIRouter, Depends
from utils.redis_cache import get_lineup, store_lineup, lineup_exists, store_player
from utils.lineup_fetcher import fetch_lineup_data, fetch_lineup_and_player
from dependencies import get_redis

router = APIRouter()

@router.get("/{team_id}")
async def get_lineup_data(team_id: int, redis=Depends(get_redis)):
    """Get the lineup data for a fantasy team."""

    # If the lineup data is already stored in Redis, retrieve it
    if await lineup_exists(redis, team_id):
        lineup_data = await get_lineup(redis, team_id)

    # Otherwise, fetch the lineup data and associated player data 
    # as the player data is likely missing in the cache too
    else:
        lineup_data, players = await fetch_lineup_and_player(team_id)
        await store_lineup(redis, team_id, lineup_data)
        for player in players:
            await store_player(redis, player['id'], player)
        
    return lineup_data

@router.put("/{team_id}")
async def update_lineup_data(team_id: int, redis=Depends(get_redis)):
    """Update the lineup data for a fantasy team."""

    # Fetch the updated lineup data
    lineup_data = await fetch_lineup_data(team_id)

    # Store the updated lineup data in Redis
    await store_lineup(redis, team_id, lineup_data)

    return lineup_data