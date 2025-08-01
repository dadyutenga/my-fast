from fastapi import Request, HTTPException, status
from fastapi.routing import APIRoute
import time
import redis

from src.config.settings import settings

r = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

class RateLimitMiddleware:
    def __init__(self, rate_limit: int = 10, per_seconds: int = 60):
        self.rate_limit = rate_limit
        self.per_seconds = per_seconds

    async def __call__(self, request: Request, call_next):
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        count = r.get(key)
        if count is None:
            r.setex(key, self.per_seconds, 1)
        elif int(count) >= self.rate_limit:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
        else:
            r.incr(key)
        response = await call_next(request)
        return response
