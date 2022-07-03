import logging

from starlette.responses import JSONResponse
from starlette.status import *
from services.apikey_found_and_active import apikey_found_and_active
from services.check_host_exists import checkHostExists
from helpers.constants import SERVICES_HOST
from helpers.utils import getHostFrom


def checkApikeyUp(apikey, destiny):
    logging.info("destiny: " + destiny)

    if apikey_found_and_active(apikey) == False:
        return False

    if destiny is None or destiny == "":
        return True

    destinyHost = getHostFrom(destiny)

    logging.info("destinyHost: " + destinyHost)

    #logging.info("constantHost: " + getHostFrom(SERVICES_HOST))

    if destinyHost != getHostFrom(SERVICES_HOST):
        aux = checkHostExists(destinyHost)
        return aux

    return True
