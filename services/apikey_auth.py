import json
import traceback

import requests
from bson import ObjectId
from fastapi import APIRouter, Request
from models.apikey import Apikey
from services.apikey_found_and_active import apikey_found_and_active
from services.auth_service import apiKeyExists
from services.check_if_api_key_up import checkApikeyUp
from services.get_available_services import getAvailableServicesFromDB
from services.logging_service import logInfo
from helpers.constants import API_KEY_UP_URL, API_KEY_DOWN_URL, REDIRECT_URL, SERVICES_HOST, SERVICES_URL, CHECK_URL, \
    MSG_NO_AUTORIZADO
from typing import List
from infrastructure.db.database import current_connection
from infrastructure.schemas.apikey import apikeyEntity, apikeysEntity
from models.apikey import Apikey
from starlette.status import *
from starlette.responses import JSONResponse
from helpers.utils import get_new_api_key, getHostFrom, getMethodFrom

import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

router = APIRouter()


def _getServices(apiKey):

    logging.info("request a" + SERVICES_URL)
    logging.debug("body.apiKey: " + str(apiKey))

    if apikey_found_and_active(str(apiKey)) == False:
        error = {"error": MSG_NO_AUTORIZADO}
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content=error)
    availableServices = getAvailableServicesFromDB()

    #return availableServices
    return JSONResponse(status_code=HTTP_200_OK, content=availableServices)


def _enableApiKey(body):
    logging.info("request a" + API_KEY_UP_URL)

    if apikey_found_and_active(str(body['apiKey'])) == False:
        error = {"error": MSG_NO_AUTORIZADO}
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content=error)

    if 'apiKeyToChange' not in body:
        apikeyToEnable = get_new_api_key()[:20]
    else:
        apikeyToEnable = str(body['apiKeyToChange'])

    existing_api_key = current_connection.find_one({"apiKey": apikeyToEnable})

    if (existing_api_key == None):
        data = {
            "apiKey": apikeyToEnable,
            "name": str(body['name']),
            "active": True,
            "creationDate": 0,
            "description": str(body['description'])
        }
        current_connection.insert_one(data)

    else:
        current_connection.update_one({"apiKey": apikeyToEnable},
                                      {"$set": {"active": True}})

    response_body = {"ok": "ok"}
    return JSONResponse(status_code=HTTP_200_OK, content=response_body)


def _disableApiKey(body):
    logging.info("request a" + API_KEY_DOWN_URL)
    if apikey_found_and_active(str(body['apiKey'])) == False:
        error = {"error": MSG_NO_AUTORIZADO}
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content=error)

    if 'apiKeyToChange' not in body:
        error = {
            "error": "El campo apikeyToDisable no existe en el cuerpo de la solicitud"}
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content=error)
    else:
        apikeyToDisable = str(body['apiKeyToChange'])

    existing_api_key = current_connection.find_one({"apiKey": apikeyToDisable})

    if (existing_api_key == None):
        error = {"error": "El servicio indicado no existe"}
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content=error)

    current_connection.update_one({"apiKey": apikeyToDisable},
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


@router.post(CHECK_URL, tags=["services"])
async def check(request: Request):
    body = await request.json()
    logInfo("request a" + CHECK_URL)
    current_apikey = str(body['apiKey'])

    try:
        current_redirect_to = str(body['redirectTo'])
    except KeyError:
        current_redirect_to = ""

    apikeyUp = checkApikeyUp(current_apikey, current_redirect_to)

    if apikeyUp is False:
        error = {"error": MSG_NO_AUTORIZADO}
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content=error)

    json_response = {
        "ok": "Autorizado",
    }

    return JSONResponse(status_code=HTTP_200_OK, content=json_response)


@router.post(REDIRECT_URL, tags=["services"])
async def redirect(request: Request):
    body = await request.json()
    logInfo("request a" + REDIRECT_URL)
    currentApikey = str(body['apiKey'])
    currentRedirectTo = str(body['redirectTo'])
    apikeyUp = checkApikeyUp(currentApikey, currentRedirectTo)

    if apikeyUp is False:
        error = {"error": MSG_NO_AUTORIZADO}
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
            # logging.info("redirectTo: " + redirectTo)

            method = getMethodFrom(redirectTo)
            param = body

            logging.info("method: " + method)

            if (method == "services"):
                logging.info("Get services")
                equalMark = redirectTo.index("=")
                param = redirectTo[equalMark + 1:]
                aux = _getServices(param)
                return aux

            elif (method == "/apikeys/up" or method == "/apikeys/createservice"):
                logging.info("Activate host")
                return _enableApiKey(body)

            else:
                logging.info("Disable host")
                return _disableApiKey(body)

        if verbRedirect == "POST":
            response = requests.post(
                url=redirectTo, json=body)

        elif verbRedirect == "GET":
            response = requests.get(
                url=redirectTo, json=body)

            logging.info(response)

        elif verbRedirect == "PATCH":
            response = requests.patch(
                url=redirectTo, json=body)

            logging.info(response)

        elif verbRedirect == "DELETE":
            response = requests.delete(
                url=redirectTo, json=body)

            logging.info(response)

        else:
            response = requests.put(
                url=redirectTo, json=body)

        json_response = json.loads(response.text)


    except Exception as e:
        logging.error(e)

        json_response = {
            "error": str(e),
        }
        status = 500

    return JSONResponse(status_code=status, content=json_response)
