import uuid
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Any, Optional

class Database:
    _instance = None

    def __new__(cls, host: str = "localhost", port: int = 27017):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.__mongo_client = MongoClient(host, port, uuidRepresentation='standard')
            cls.db_name = "restaurant"
            cls.database = cls.__mongo_client[cls.db_name]
        return cls._instance

    def __del__(self):
        self.__mongo_client.close()

    def close(self):
        self.__del__()

    def get_collection(self, collection_name: str) -> Collection:
        return self.database[collection_name]

    async def fetch_one(self, collection_name: str, query: dict) -> Optional[dict[str, Any]]:
        collection = self.get_collection(collection_name)
        return collection.find_one(query)

    async def fetch_all(self, collection_name: str, query: dict) -> list[dict[str, Any]]:
        collection = self.get_collection(collection_name)
        return list(collection.find(query))

    async def execute(self, collection_name: str, query: dict, operation: Any) -> None:
        collection = self.get_collection(collection_name)
        if operation == 'insert':
            collection.insert_one(query)
        elif operation == 'update':
            collection.update_one(query['filter'], query['update'])
        elif operation == 'delete':
            collection.delete_one(query)
