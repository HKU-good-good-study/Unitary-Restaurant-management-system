from pymongo import MongoClient
class Database:
    _instance = None

    def __new__(cls, host: str = "localhost", port: int = 27017):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.__mongo_client = MongoClient(host, port)
            cls.db_name = "restaurant"
            cls.database = cls.__mongo_client[cls.db_name]
        return cls._instance
    
    def __del__(self):
        return self.__mongo_client.close()
    
    def close(self):
        return self.__del__()