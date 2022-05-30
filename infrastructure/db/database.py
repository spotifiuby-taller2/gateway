from bson import ObjectId
from pymongo import MongoClient
from mongoengine import connect
import os

from models.apikey import Apikey

try:
    os.environ['IN_PRODUCTION']
    # connection = connect(db="spotify", host="localhost", port=27017)
    connection = MongoClient('localhost', 27017)
    current_connection = connection.spotify.apikey
except KeyError:
    connection = MongoClient("mongodb+srv://taller2:rensenbrinklepegoalpalo@cluster0.nyzrv.mongodb.net/?retryWrites=true&w=majority")
    current_connection = connection.myFirstDatabase.apikey

if connection is not None:
    print("CONECTADO A LA BASE DE DATOS")

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
