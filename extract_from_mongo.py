import pymongo as pm

def get_cursor():

    Client = pm.MongoClient(r'mongodb://localhost:27017/')
    db = Client["practice_data"]
    collection = db["tickets"]

    cursor = collection.find().batch_size(1)

    return cursor 
