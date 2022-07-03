from infrastructure.db.database import current_connection
from infrastructure.schemas.apikey import apikeyEntity

import logging

logging.basicConfig(level=logging.DEBUG)


def apikey_found_and_active(apikey):
    result = current_connection.find_one({"apiKey": apikey})

    if result is None:
        return False

    return (apikeyEntity(result))['active']
