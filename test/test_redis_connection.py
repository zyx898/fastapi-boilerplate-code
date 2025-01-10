import pytest
import asyncio
import sys
import os
import json

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.redis import RedisManager, CacheService

@pytest.mark.asyncio
async def test_redis_connection():
    """Test Redis connection and basic CRUD operations"""
    try:
        # Get Redis client
        redis_client = await RedisManager.get_client()
        cache_service = CacheService()
        
        # Test data write
        test_data = {"test_key": "test_value"}
        await cache_service.set_cache("test_key", test_data)
        print("✅ Set operation successful")
        
        # Test data read
        found_data = await cache_service.get_cache("test_key")
        assert found_data is not None
        assert found_data["test_key"] == "test_value"
        print("✅ Get operation successful")
        
        # Test data update
        updated_data = {"test_key": "updated_value"}
        await cache_service.set_cache("test_key", updated_data)
        updated_found = await cache_service.get_cache("test_key")
        assert updated_found["test_key"] == "updated_value"
        print("✅ Update operation successful")
        
        # Test TTL set
        await cache_service.set_cache("ttl_key", {"temp": "data"}, ttl=10)
        ttl_data = await cache_service.get_cache("ttl_key")
        assert ttl_data is not None
        print("✅ TTL set operation successful")
        
        # Test data delete
        await cache_service.delete_cache("test_key")
        deleted_data = await cache_service.get_cache("test_key")
        assert deleted_data is None
        print("✅ Delete operation successful")
        
        print("🎉 All Redis operations completed successfully!")
        
    except Exception as e:
        print("❌ Failed to perform Redis operations")
        print(f"Error: {str(e)}")
        raise
    finally:
        # Close connection
        await RedisManager.close()

if __name__ == "__main__":
    asyncio.run(test_redis_connection())