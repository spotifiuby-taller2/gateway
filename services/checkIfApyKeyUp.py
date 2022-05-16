
from starlette.responses import JSONResponse
from starlette.status import *
from services.apikeyFoundAndActive import apikey_found_and_active
from services.checkHostExists import checkHostExists
from utils.constants import SERVICES_HOST
from utils.utils import getHostFrom


def checkApikeyUp(apikey, destiny):
    print("destiny: " + destiny)

    if apikey_found_and_active(apikey) == False:
        error = {"error": "No Autorizado"}
        return False

    if destiny is None:
        return True
# LIO
    destinyHost = getHostFrom(destiny)

    if destinyHost != getHostFrom(SERVICES_HOST):
        aux = checkHostExists(destinyHost)
        return aux

    return True
