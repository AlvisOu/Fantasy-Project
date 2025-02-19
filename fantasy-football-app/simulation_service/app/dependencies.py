import aioredis

# Redis connection settings
REDIS_HOST = "localhost"
REDIS_PORT = 6379

async def get_redis():
    """ Dependency injection to get a redis connection connection """
    redis = await aioredis.create_redis_pool(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)
    try:
        yield redis
    finally:
        await redis.close()
