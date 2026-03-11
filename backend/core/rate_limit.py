from fastapi import Request, HTTPException
from db.redis import redis_client

async def rate_limit(request: Request, limit=5, window=60):
    key = f"rl:{request.client.host}"
    count = await redis_client.incr(key)
    limit = 5
    if count == 1:
        await redis_client.expire(key, window)
    if count > limit:
        raise HTTPException(429, "Too many requests")
