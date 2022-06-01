from data.constants import REDIRECT_URL, API_KEY_DOWN_URL, API_KEY_UP_URL, SERVICES_URL
from src.services.apyKeyExists import apiKeyExists
from src.others.utils import getSHAof
import os
import logging



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ApiKeyService():
    def defineEvents(app):

        @app.post(REDIRECT_URL)
        async def redirect():
            logger.info("Request to /redirect")
            if(not await apiKeyExists):
                return "error"
            else:
                return "ok"

        @app.post(API_KEY_DOWN_URL)
        async def disableApiKey():
            logger.info("Request to /apikey/down")            
            return "disable"
        
        @app.post(API_KEY_UP_URL) 
        async def enableApiKey():
            logger.info("Request to /apikey/up")            
            return "enable"
        
        @app.get(SERVICES_URL)
        async def getServices():
            logger.info("Request to /services")            
            return "services"
    
    def getNewApiKey():
        return getSHAof(os.urandom(20).hex())