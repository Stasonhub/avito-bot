from pymongo import MongoClient
from config import mongo_url

class DB:
	def __init__(self):
		self.client = MongoClient(mongo_url)

	def get_collection(self, collection_name):
		return self.client[collection_name]

	def add_document(self, collection, document):
		collection.insert_one(document).inserted_id

if __name__ == '__main__':
	db = DB()
	