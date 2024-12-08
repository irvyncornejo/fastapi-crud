from infrastructure.repositories.mongo_repository import MongoRepository
from bson import ObjectId


class UserRepository(MongoRepository):
    def __init__(self, db_name, collection_name, use_async=False):
        super().__init__(db_name, collection_name, use_async)

    def retrieve_users(self):
        collection = self._get_collection()
        return collection.find({'delete': False})

    def retrieve_user_by_id(self, id:ObjectId):
        collection = self._get_collection()
        user = collection.find_one({'_id': id})
        return user

    def retrieve_user_by_email(self, email:str):
        collection = self._get_collection()
        user = collection.find_one({'email': email})
        return user
 
    def create_user(self, data: dict):
        collection = self._get_collection()
        user = collection.insert_one(data)
        return self.retrieve_user_by_id(user.inserted_id)

    def update_user(self, id:ObjectId, data):
        collection = self._get_collection()
        user = collection.find_one_and_update(
            {'_id': id},
            {'$set': data}
        )

        return user

    def delete_user(self, id:ObjectId):
        collection = self._get_collection()
        response = collection.delete_one({'_id': id})
        return response.deleted_count

