import asyncio
import json
import traceback

import aioredis
from sshtunnel import SSHTunnelForwarder

from core.config import settings  # Assuming settings are defined elsewhere


class RedisManager:
    _client: aioredis.Redis = None
    _tunnel: SSHTunnelForwarder = None
    _lock = asyncio.Lock()  # Add a lock for thread safety

    @classmethod
    async def get_client(cls) -> aioredis.Redis:
        async with cls._lock:  # Use lock to prevent race conditions
            if cls._client is None:  # Check inside the lock
                try:
                    if cls._tunnel is None:
                        cls._tunnel = SSHTunnelForwarder(
                            (settings.SSH_HOST, settings.SSH_PORT),
                            ssh_username=settings.SSH_USERNAME,
                            ssh_password=settings.SSH_PASSWORD,
                            remote_bind_address=(settings.REDIS_HOST, settings.REDIS_PORT),
                        )
                        cls._tunnel.start()

                    cls._client = await aioredis.from_url(
                        url=f"redis://localhost:{cls._tunnel.local_bind_port}",
                        encoding="utf-8",
                        decode_responses=True,
                        db=settings.REDIS_DB,
                    )
                    print(f"Connected to Redis at {cls._tunnel.local_bind_port}")
                    print(f"Redis DB: {settings.REDIS_DB}")

                except Exception as e:
                    print(f"Failed to connect to Redis: {traceback.format_exc()}")
                    raise  # Reraise the exception after printing the traceback

            return cls._client  # Return client even if it already exists

    @classmethod
    async def close(cls):
        async with cls._lock:
            if cls._client:
                await cls._client.close()
                cls._client = None
            if cls._tunnel:
                cls._tunnel.stop()
                cls._tunnel = None


class CacheService:
    @staticmethod
    async def get_cache(key: str):
        redis = await RedisManager.get_client()
        value = await redis.get(key)
        try:  # Attempt to parse JSON, return None if it fails
            return json.loads(value) if value else None
        except json.JSONDecodeError:
            return None

    @staticmethod
    async def set_cache(key: str, value: any, ttl: int = None):
        redis = await RedisManager.get_client()
        await redis.set(key, json.dumps(value), ex=ttl)

    @staticmethod
    async def delete_cache(key: str):
        redis = await RedisManager.get_client()
        await redis.delete(key)

