import asyncio, logging
from fastapi import APIRouter, Depends, HTTPException
from utils.redis_cache import get_lineup, store_lineup, lineup_exists, store_player
from utils.lineup_fetcher import fetch_lineup_data, fetch_lineup_and_player
from dependencies import get_redis

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/{team_id}")
async def get_lineup_data(team_id: int, redis=Depends(get_redis)):
    """Get the lineup data for a fantasy team."""
    try:

        # If the lineup data is already stored in Redis, retrieve it
        if await lineup_exists(redis, team_id):
            lineup_data = await get_lineup(redis, team_id)
            logger.info(f"Returned cached lineup for team {team_id}")
            return {"message": "Lineup retrieved from cache", "lineup": lineup_data}

        # Otherwise, fetch the lineup data and associated player data 
        # as the player data is likely missing in the cache too
        lineup_data, players = await fetch_lineup_and_player(team_id)
        await store_lineup(redis, team_id, lineup_data)
        for player in players:
            await store_player(redis, player['id'], player)

        logger.info(f"Fetched and stored new lineup for team {team_id}. Also fetched and stored player data.")
        return {"message": "Fetched and cached lineup and player data", "lineup": lineup_data}
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the lineup data.")

@router.put("/{team_id}")
async def update_lineup_data(team_id: int, redis=Depends(get_redis)):
    """Update the lineup data for a fantasy team."""

    try:
        # Fetch the updated lineup data
        lineup_data = await fetch_lineup_data(team_id)

        # Store the updated lineup data in Redis
        await store_lineup(redis, team_id, lineup_data)
        logger.info(f"Updated lineup for team {team_id} in Redis.")

        return {"message": "Updated lineup in cache", "lineup": lineup_data}

    except Exception as e:
        logger.error(f"Unexpected error updating lineup for team {team_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")