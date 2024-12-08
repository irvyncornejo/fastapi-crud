from typing import Union
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from settings import SETTINGS, log


class MongoRepository:
    def __init__(
        self,
        db_name:Union[str, None],
        collection_name:Union[str, None],
        use_async=False
    )->None:
        self.db_name = db_name
        self.collection_name = collection_name
        self.string_conection = SETTINGS.mongo_conn_str
        self.use_async = use_async

    def _get_connection(self)->Union[MongoClient, AsyncIOMotorClient]:
        if not self.use_async:
            conn = MongoClient(self.string_conection)
        else:
            conn = AsyncIOMotorClient(self.string_conection)
        return conn

    def _get_collection(self):
        conn = self._get_connection()
        db = conn[self.db_name]
        return db[self.collection_name]

    def start_db(self):
        conn = self._get_connection()
        try:
            dbs = conn.list_database_names()
            if self.db_name not in dbs:
                db = conn[self.db_name]
                db.create_collection(self.collection_name)
                conn.close()
                return 0
            else:
                db = conn[self.db_name]
                collections = db.list_collection_names()
                if self.collection_name not in collections:
                    db.create_collection(self.collection_name)
                conn.close()
                return 0

        except Exception as e:
            log.error(f'Error al inicializar la db {e}')