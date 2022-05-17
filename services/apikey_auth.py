import json
import requests
from bson import ObjectId
from fastapi import APIRouter, Request
from models.apikey import Apikey
from services.apikeyFoundAndActive import apikey_found_and_active
from services.auth_service import apiKeyExists
from services.checkIfApyKeyUp import checkApikeyUp
from services.getAvailableServices import getAvailableServicesFromDB
from utils.constants import API_KEY_UP_URL, API_KEY_DOWN_URL, REDIRECT_URL, SERVICES_HOST, SERVICES_URL, JSON_HEADER
from typing import List
from infrastructure.db.database import current_connection
from infrastructure.schemas.apikey import apikeyEntity, apikeysEntity
from models.apikey import Apikey
from starlette.status import *
from starlette.responses import JSONResponse
from utils.utils import get_new_api_key, getHostFrom, getMethodFrom

import logging
logging.basicConfig(level=logging.DEBUG)


router = APIRouter()


# -----------------------------------------------------


@router.post("/agregarapikey", response_model=Apikey, tags=["apikeys"])
def create_apikey(apikey: Apikey):
    new_apikey = dict(apikey)
    del new_apikey["id"]
    id = current_connection.insert_one(new_apikey).inserted_id
    return str(id)


# ***************************************************************************


def _getServices(apiKey):

    logging.info("request a" + SERVICES_URL)
    logging.debug("body.apiKey: " + str(apiKey))

    if apikey_found_and_active(str(apiKey)) == False:
        error = {"error": "No Autorizado"}
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content=error)
    availableServices = getAvailableServicesFromDB()
    print(availableServices)
    return JSONResponse(status_code=HTTP_200_OK, content=availableServices)


def _enableApiKey(body):
    logging.info("request a" + API_KEY_UP_URL)
    logging.debug("body.apiKey: " + str(body['apiKey']))

    if apikey_found_and_active(str(body['apiKey'])) == False:
        error = {"error": "No Autorizado"}
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content=error)

    if 'apikeyToEnable' not in body:
        apikeyToEnable = get_new_api_key()[:20]
        logging.debug("apiKeyToEnable: " + apikeyToEnable)
    else:
        apikeyToEnable = str(body['apikeyToEnable'])

    existing_api_key = current_connection.find_one({"apiKey": apikeyToEnable})

    if (existing_api_key == None):
        data = {
            "apiKey": apikeyToEnable,
            "name": str(body['name']),
            "active": True,
            "creation_date": 0,
            "description": str(body['description'])
        }
        current_connection.insert_one(data)
    else:
        current_connection.update_one({"apikey": apikeyToEnable},
                                      {"$set": {"active": True}})

    response_body = {"ok": "ok"}
    return JSONResponse(status_code=HTTP_200_OK, content=response_body)


def _disableApiKey(body):
    logging.info("request a" + API_KEY_DOWN_URL)
    if apikey_found_and_active(str(body['apiKey'])) == False:
        error = {"error": "No Autorizado"}
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content=error)

    if 'apikeyToDisable' not in body:
        error = {
            "error": "El campo apikeyToDisable no existe en el cuerpo de la solicitud"}
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content=error)
    else:
        apikeyToDisable = str(body['apikeyToDisable'])

    existing_api_key = current_connection.find_one({"apikey": apikeyToDisable})

    if (existing_api_key == None):
        error = {"error": "El servicio indicado no existe"}
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content=error)

    current_connection.update_one({"apikey": apikeyToDisable},
                                  {"$set": {"active": False}})

    response_body = {"ok": "ok"}
    return JSONResponse(status_code=HTTP_200_OK, content=response_body)


@router.post(API_KEY_UP_URL, tags=["services"])
async def enableApiKey(request: Request):
    body = await request.json()
    return _enableApiKey(body)


@router.post(API_KEY_DOWN_URL, tags=["services"])
async def disableApiKey(request: Request):
    body = await request.json()
    return _disableApiKey(body)


@router.get(SERVICES_URL, response_model=List[Apikey], tags=["services"])
async def getServices(apiKey: str, request: Request):
    aux = _getServices(apiKey)
    return aux


methodToCall = {
    API_KEY_UP_URL: _enableApiKey,
    API_KEY_DOWN_URL: _disableApiKey,
    SERVICES_URL: _getServices
}


@router.post(REDIRECT_URL, tags=["services"])
async def redirect(request: Request):
    body = await request.json()
    logging.info("request a" + REDIRECT_URL)
    currentApikey = str(body['apiKey'])
    currentRedirectTo = str(body['redirectTo'])
    apikeyUp = checkApikeyUp(currentApikey, currentRedirectTo)

    if apikeyUp is False:
        error = {"error": "No Autorizado"}
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content=error)

    redirectParams = ""
    if 'redirectParams' in body:
        redirectParams = str(body['redirectParams'])

    if 'redirectTo' in body:
        redirectTo = str(body['redirectTo']) + redirectParams

    if 'verbRedirect' in body:
        verbRedirect = str(body['verbRedirect'])

    body['redirectTo'] = ""
    body['verbRedirect'] = ""
    body['method'] = verbRedirect

    requestData = {
        "method": verbRedirect,
    }

    status = 200
    try:
        if getHostFrom(redirectTo) == getHostFrom(SERVICES_HOST):
            method = getMethodFrom(redirectTo)
            param = body
            if (method == "services"):
                equalMark = redirectTo.index("=")
                param = redirectTo[equalMark + 1:]
                aux = _getServices(param)
                return aux

            elif (method == "up"):
                return _enableApiKey(param)

            else:
                return _disableApiKey(param)

        if verbRedirect == "POST":
            response = requests.post(
                url=redirectTo, json=body)
        elif verbRedirect == "GET":
            response = requests.get(
                url=redirectTo, json=body)

            logging.info(response)

        else:
            response = requests.put(
                url=redirectTo, json=body)

        json_response = json.loads(response.text)
        print(json_response)

        #status = response.status_code
        # print(status)

    except Exception as e:

        json_response = {
            "error": str(e),
        }
        print("no entro")
        status = 500
    return JSONResponse(status_code=status, content=json_response)
