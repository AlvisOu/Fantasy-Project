import aioredis

REDIS_URL = "redis://localhost:6379"

async def get_redis():
    """ Dependency injection to get a redis connection connection """
    redis = await aioredis.create_redis_pool(REDIS_URL, decode_responses=True)
    try:
        yield redis
    finally:
        await redis.close()
