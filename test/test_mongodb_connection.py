import pytest
import asyncio
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.mongodb import DatabaseManager

@pytest.mark.asyncio
async def test_mongodb_connection():
    """Test MongoDB connection and basic CRUD operations"""
    try:
        # Connect to database
        database_client = await DatabaseManager.get_client()
        
        # Get test database and collection
        test_db = database_client.get_database('test')
        test_collection = test_db.test_collection
        
        # Test data insertion
        test_doc = {"test_key": "test_value"}
        insert_result = await test_collection.insert_one(test_doc)
        assert insert_result.inserted_id is not None
        print("✅ Insert operation successful")
        
        # Test data retrieval 
        found_doc = await test_collection.find_one({"test_key": "test_value"})
        assert found_doc is not None
        assert found_doc["test_key"] == "test_value"
        print("✅ Find operation successful")
        
        # Test data update
        update_result = await test_collection.update_one(
            {"test_key": "test_value"},
            {"$set": {"test_key": "updated_value"}}
        )
        assert update_result.modified_count == 1
        print("✅ Update operation successful")
        
        # Test data deletion
        delete_result = await test_collection.delete_one({"test_key": "updated_value"})
        assert delete_result.deleted_count == 1
        print("✅ Delete operation successful")
        
        print("🎉 All MongoDB operations completed successfully!")
        
    except Exception as e:
        print("❌ Failed to perform MongoDB operations")
        print(f"Error: {str(e)}")
        raise
    finally:
        # Close connection
        await DatabaseManager.close()

if __name__ == "__main__":
    asyncio.run(test_mongodb_connection())