from bson import ObjectId
from pymongo import MongoClient
from mongoengine import connect

from models.apikey import Apikey

# connection = connect(db="spotify", host="localhost", port=27017)
connection = MongoClient('localhost', 27017)

current_connection = connection.spotify.apikey


'''
def ApiKeyExists(id):
    result = connection.spotify.apikey.count_documents({"_id": ObjectId(id)})
    print("apikeyExistsResult: " + result)
    return result

def check_api_key(self, api_key):

    if api_key == self.api_key:
        return True
    raise ApiKeyError()
# ApiKeyExists("62648bba42103357886bafba")
'''
