import asyncio
import os
import sys
import traceback

import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from sshtunnel import SSHTunnelForwarder

from core.config import settings


class DatabaseManager:  # Renamed for clarity
    _client: AsyncIOMotorClient = None
    _tunnel: SSHTunnelForwarder = None
    _lock = asyncio.Lock()

    @classmethod
    async def get_client(cls) -> AsyncIOMotorClient:
        async with cls._lock:
            if cls._client is None:
                try:
                    if cls._tunnel is None:
                        cls._tunnel = SSHTunnelForwarder(
                            (settings.SSH_HOST, settings.SSH_PORT),
                            ssh_username=settings.SSH_USERNAME,
                            ssh_password=settings.SSH_PASSWORD,
                            remote_bind_address=(settings.MONGODB_HOST, settings.MONGODB_TUNNEL_PORT),
                        )
                        cls._tunnel.start()

                    connection_string = f"mongodb://{settings.MONGODB_USERNAME}:{settings.MONGODB_PASSWORD}@localhost:{cls._tunnel.local_bind_port}"

                    cls._client = AsyncIOMotorClient(
                        connection_string,
                        serverSelectionTimeoutMS=30000,
                        tlsCAFile=certifi.where() if settings.MONGODB_USE_TLS else None,  # Conditional TLS usage
                    )

                    try:
                        await cls._client.admin.command("ping")  # Use ping command for simpler check
                        print("Successfully connected to MongoDB.")
                    except Exception as e:
                        print(f"Failed to connect to MongoDB: {traceback.format_exc()}")
                        if cls._tunnel:
                            cls._tunnel.stop()
                        raise

                except Exception as e:
                    print(f"Failed to establish SSH tunnel: {traceback.format_exc()}")
                    if cls._tunnel:
                        cls._tunnel.stop()
                    raise

            return cls._client

    @classmethod
    async def close(cls):
        async with cls._lock:
            if cls._client:
                cls._client.close()
                cls._client = None
            if cls._tunnel:
                cls._tunnel.stop()
                cls._tunnel = None
