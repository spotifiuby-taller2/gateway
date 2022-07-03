from bson import ObjectId
from pymongo import MongoClient
from mongoengine import connect
import os

from infrastructure.db.migrations import run_migrations
from models.apikey import Apikey
from services.logging_service import logInfo
from helpers.constants import RUN_MIGRATIONS

try:
    os.environ['IN_PRODUCTION']
    connection = MongoClient(
        "mongodb+srv://taller2:rensenbrinklepegoalpalo@cluster0.nyzrv.mongodb.net/?retryWrites=true&w=majority")
    current_connection = connection.myFirstDatabase.apikey
    logInfo("Connected to Atlas remote database")

except KeyError:
    connection = MongoClient('localhost', 27017)
    current_connection = connection.spotify.apikey
    logInfo("Connected to local database")


if connection is not None:
    logInfo("CONECTADO A LA BASE DE DATOS")

try:
    os.environ['IN_PRODUCTION']
    RUN_MIGRATIONS = True
except KeyError:
    pass

if RUN_MIGRATIONS:
    logInfo("Corriendo migraciones...")
    run_migrations(current_connection)

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
