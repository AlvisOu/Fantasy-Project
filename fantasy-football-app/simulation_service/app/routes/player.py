import logging
from fastapi import APIRouter, Depends, HTTPException
from utils.redis_cache import store_player, player_exists, get_player
from utils.lineup_fetcher import fetch_player_data
from dependencies import get_redis

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/{player_id}")
async def get_player_data(player_id: int, redis=Depends(get_redis)):
    """Get the player data."""
    try: 
        # If the player data is already stored in Redis, retrieve it
        if await player_exists(redis, player_id):
            player_data = await get_player(redis, player_id)
            logger.info(f"Returned cached player data for player {player_id}")
            return {"message": "Player data retrieved from cache", "player": player_data}

        # Otherwise, fetch the player data
        player_data = await fetch_player_data(player_id)
        await store_player(redis, player_id, player_data)
        logger.info(f"Fetched and stored new player data for player {player_id}.")
        return {"message": "Fetched and cached player data", "player": player_data}
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the player data.")

@router.put("/{player_id}")
async def update_player_data(player_id: int, redis=Depends(get_redis)):
    """Update the player data."""
    
    try:
        # Fetch the updated player data
        player_data = await fetch_player_data(player_id)
        
        # Store the updated player data in Redis
        await store_player(redis, player_id, player_data)
        logger.info(f"Updated player data for player {player_id} in Redis.")

        return {"message": "Updated player data in cache", "player": player_data}
    
    except Exception as e:
        logger.error(f"Unexpected error updating player data for player {player_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")