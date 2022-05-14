import logging
from models.apikey import Apikey
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# def getNewApiKey():
#    return getSHAof(os.urandom(20).hex())


async def apiKeyExists(apikey):
    response = await Apikey


def checkApiKeyUp(apikey):
    return  # apikey_active(apikey)
