import logging
from infrastructure.db.database import current_connection
import logging

from utils.utils import is_production

logging.basicConfig(level=logging.DEBUG)


def checkHostExists(destinyHost):
    if "localhost" in destinyHost and not is_production():
        return True

    response = current_connection.find_one(
        {"description": destinyHost, "active": True})

    if response is None:
        logging.debug("Destino no encontrado entre los hosts activos.")
        return False

    return response is not None
