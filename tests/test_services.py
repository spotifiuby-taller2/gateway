import pytest

from infrastructure.schemas.apikey import apikeyEntity
from services.apikey_found_and_active import apikey_found_and_active
from services.apikey_auth import _getServices, getServices, _enableApiKey, enableApiKey, check, _disableApiKey

from unittest.mock import patch

from main import app

from fastapi.testclient import TestClient

import sys

from services.check_host_exists import checkHostExists
from services.check_if_api_key_up import checkApikeyUp
from services.get_available_services import getAvailableServicesFromDB

sys.path.append('../helpers/constants.py')

from helpers import constants

client = TestClient(app)

# pytest only detects functions or classes that to start with "test"
# and are contained in a file with a name starting with "test".

# To run tests showing print()
# python3 -m pytest -s

# To run tests with coverage
# python3 -m pytest --cov=./services --cov-report xml

dummy_value = 'patched dummy value'


@patch("services.apikey_auth.apikey_found_and_active", return_value=True)
@patch("services.apikey_auth.getAvailableServicesFromDB", return_value=dummy_value)
def test_01_get_services_success(*args):
    response = _getServices("request")

    # The structure is actual = expected, where expected is a hardcode
    assert response.status_code == 200
    assert dummy_value in str(response.body)


dummy_value_2 = "one of my dummy values"


@pytest.mark.asyncio
@patch("services.apikey_auth._getServices", return_value=dummy_value_2)
async def test_02_get_services(*args):
    response = await getServices("request", None)

    assert response == dummy_value_2


@patch("services.apikey_auth.apikey_found_and_active", return_value=False)
def test_03_get_services_cannot_access_due_to_unauthorized_users(*args):
    response = _getServices("request")

    # The structure is actual = expected, where expected is a hardcode
    assert response.status_code == 401


# dummy_data = {'apiKey':202020}

dummy_data = {
    "apiKey": 202020,
    "name": "dummy",
    "active": True,
    "creationDate": 0,
    "description": "dummy"
}


@patch("services.apikey_auth.apikey_found_and_active", return_value=False)
def test_04_enableApiKey_cannot_access_due_to_unauthorized_users(*arg):
    response = _enableApiKey(dummy_data)

    assert response.status_code == 401
    assert "No autorizado" in str(response.body)


@patch("services.apikey_auth.apikey_found_and_active", return_value=True)
@patch("services.apikey_auth.current_connection.find_one", return_value=dummy_value)
@patch("services.apikey_auth.current_connection.update_one")
def test_05_enableApiKeyExistingApikey(*arg):
    response = _enableApiKey(dummy_data)

    assert response.status_code == 200
    assert "ok" in str(response.body)


@patch("services.apikey_auth.apikey_found_and_active", return_value=True)
@patch("services.apikey_auth.current_connection.find_one", return_value=None)
@patch("services.apikey_auth.current_connection.insert_one")
def test_06_enableApiKeyNonExistingApikey(*arg):
    response = _enableApiKey(dummy_data)

    assert response.status_code == 200
    assert "ok" in str(response.body)


@patch("services.apikey_auth.apikey_found_and_active", return_value=False)
def test_07_disableApiKeyNonExistingApikey(*arg):
    response = _disableApiKey(dummy_data)

    assert response.status_code == 401
    assert "No autorizado" in str(response.body)


@patch("services.apikey_auth.apikey_found_and_active", return_value=True)
def test_08_disableApiKeyBadRequest(*arg):
    response = _disableApiKey(dummy_data)

    assert response.status_code == 400
    assert "El campo apikeyToDisable no existe en el cuerpo de la solicitud" in str(response.body)


dummy_data_2 = {
    "apiKey": 202020,
    "name": "dummy",
    "active": True,
    "creationDate": 0,
    "description": "dummy",
    "apiKeyToChange": 202021
}
dummy_data_changed = {
    "apiKey": 202021,
    "name": "dummy",
    "active": True,
    "creationDate": 0,
    "description": "dummy"
}


@patch("services.apikey_auth.apikey_found_and_active", return_value=True)
@patch("services.apikey_auth.current_connection.find_one", return_value=dummy_data_2)
@patch("services.apikey_auth.current_connection.update_one", return_value=dummy_data_changed)
def test_09_disableApiKeySuccessfully(*arg):
    response = _disableApiKey(dummy_data_2)

    assert response.status_code == 200
    assert "ok" in str(response.body)


@patch("services.apikey_auth.apikey_found_and_active", return_value=True)
@patch("services.apikey_auth.current_connection.find_one", return_value=None)
def test_10_disableApiKeyServiceDoesNotExist(*arg):
    response = _disableApiKey(dummy_data_2)

    assert response.status_code == 404
    assert "El servicio indicado no existe" in str(response.body)


# ----------------------------------------------------------------

@pytest.mark.asyncio
@patch("services.apikey_auth._enableApiKey", return_value="ok")
async def test_11_enableApiKey(request):
    response = client.post(constants.API_KEY_UP_URL, json={"data": "data"})

    assert response.json() == "ok"


dummy_value_3 = "Dummy value 3"


@patch("services.apikey_auth._disableApiKey", return_value=dummy_value_3)
def test_12_disable_api_key(*args):
    response = client.post(constants.API_KEY_DOWN_URL, json={"data": "data"})

    assert response.json() == dummy_value_3


@pytest.mark.asyncio
@patch("services.apikey_auth.checkApikeyUp", return_value=True)
async def test_13_check(request):
    response = client.post(constants.CHECK_URL, json=dummy_data)

    assert "ok" in str(response.json())


@pytest.mark.asyncio
@patch("services.apikey_auth.checkApikeyUp", return_value=False)
async def test_14_check_unauthorized(request):
    response = client.post(constants.CHECK_URL, json=dummy_data)

    assert "No autorizado" in str(response.json())


dummy_data_redirect = {
    "apiKey": 202020,
    "name": "dummy",
    "active": True,
    "redirectTo": "service",
    "description": "dummy",
    "verbRedirect": "POST",
}


@pytest.mark.asyncio
@patch("services.apikey_auth.checkApikeyUp", return_value=False)
async def test_15_redirect_unauthorized(request):
    response = client.post(constants.REDIRECT_URL, json=dummy_data_redirect)

    assert "No autorizado" in str(response.json())


@patch("services.apikey_auth.checkApikeyUp", return_value=True)
@patch("services.apikey_auth.getHostFrom", return_value="value")
async def test_16_redirect(*args):
    response = client.post(constants.REDIRECT_URL, json=dummy_data_redirect)

    assert "not found" in str(response.json())


@patch("services.apikey_found_and_active.current_connection.find_one", return_value=None)
async def test_17_apiKey_found_and_active(apikey):
    active = apikey_found_and_active(apikey)

    assert active is False


@pytest.mark.asyncio
@patch("services.apikey_found_and_active.current_connection.find_one", return_value=None)
async def test_18_checkHostExistsIsFalse(*args):
    hostExists = checkHostExists(dummy_value)

    assert hostExists is False


@pytest.mark.asyncio
@patch("services.apikey_found_and_active.current_connection.find_one", return_value="something")
async def test_19_checkHostExists(*args):
    hostExists = checkHostExists(dummy_value)

    assert hostExists is True


@pytest.mark.asyncio
@patch("services.check_if_api_key_up.apikey_found_and_active", return_value=False)
async def test_20_checkApikeyUpNotActive(*args):
    apikeyUp = checkApikeyUp(dummy_value, dummy_value)

    assert apikeyUp is False


@pytest.mark.asyncio
@patch("services.check_if_api_key_up.apikey_found_and_active", return_value=True)
async def test_21_checkApikeyUpDestinyIsNone(*args):
    apikeyUp = checkApikeyUp(dummy_value, "")

    assert apikeyUp is True


@pytest.mark.asyncio
@patch("services.apikey_found_and_active.current_connection.find_one", return_value="http://something/")
@patch("services.check_if_api_key_up.apikey_found_and_active", return_value=True)
async def test_22_checkApikeyUpDestinySameAsHost(*args):
    apikeyUp = checkApikeyUp(dummy_value, "http://something/")

    assert apikeyUp is True


'''
dummy_list = [['_id':1],['_id'],['_id']]

@pytest.mark.asyncio
@patch("services.getAvailableServices.current_connection.find", return_value= dummy_list)
async def test_18_checkApikeyUpDestinyIsNone(*args):

    services = getAvailableServicesFromDB()

    assert services == dummy_list
'''
