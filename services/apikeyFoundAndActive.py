from infrastructure.db.database import current_connection
from infrastructure.schemas.apikey import apikeyEntity

import logging
logging.basicConfig(level=logging.DEBUG)


def apikey_found_and_active(apikey):
    apikey = current_connection.find_one({"apikey": apikey})
    if (apikey == None):
        return False
    return (apikeyEntity(apikey))['active']
