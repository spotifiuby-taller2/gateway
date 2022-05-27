import logging
from infrastructure.db.database import current_connection
import logging
logging.basicConfig(level=logging.DEBUG)


def checkHostExists(destinyHost):
    response = current_connection.find_one(
        {"description": destinyHost}, {"active": True})

    if response is None:
        logging.debug("No se pudo consultar las api key existentes")
        return False

    return response is not None
