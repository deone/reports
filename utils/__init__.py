from pymongo import MongoClient

def get_collection(collection_name):
    client = MongoClient()
    db = client.reports
    return db[collection_name]