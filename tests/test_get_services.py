import pytest

from services.apikey_auth import _getServices, getServices, _enableApiKey
from unittest.mock import patch

# pytest only detects functions or classes that to start with "test"
# and are contained in a file with a name starting with "test".

# To run tests showing print()
# python3 -m pytest -s

# To run tests with coverage
# python3 -m pytest --cov=./services --cov-report xml

dummy_value = 'patched dummy value'


@patch("services.apikey_auth.apikey_found_and_active", return_value=True)
@patch("services.apikey_auth.getAvailableServicesFromDB", return_value=dummy_value)
def test_get_services_success(*args):
    response = _getServices("request")

    # The structure is actual = expected, where expected is a hardcode
    assert response.status_code == 200
    assert dummy_value in str(response.body)


dummy_value_2 = "one of my dummy values"


@pytest.mark.asyncio
@patch("services.apikey_auth._getServices", return_value=dummy_value_2)
async def test_get_services(*args):
    response = await getServices("request", None)

    assert response == dummy_value_2

@patch("services.apikey_auth.apikey_found_and_active", return_value=False)
def test_get_services_cannot_access_due_to_unauthorized_users(*args):
    response = _getServices("request")

    # The structure is actual = expected, where expected is a hardcode
    assert response.status_code == 401



dummy_data = {'apiKey':202020}
@patch("services.apikey_auth.apikey_found_and_active", return_value=False)
def test_enableApiKey_cannot_access_due_to_unauthorized_users(*arg):
    response = _enableApiKey(dummy_data)

    assert response.status_code == 401


@patch("services.apikey_auth.apikey_found_and_active", return_value=True)
@patch("services.apikey_auth.current_connection.find_one", return_value=dummy_value)
@patch("services.apikey_auth.current_connection.update_one")

def test_enableApiKey(*arg):
    response = _enableApiKey(dummy_data)

    assert response.status_code == 200



@pytest.mark.asyncio
@patch("services.apikey_auth._getServices", return_value=dummy_value_2)
async def test_enableServices(*args):
    response = await getServices("request", None)

    assert response == dummy_value_2