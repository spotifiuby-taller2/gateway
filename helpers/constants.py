import os
from dotenv import load_dotenv
import pathlib

#del os.environ['SERVICES_HOST']

current_path = str(pathlib.Path(__file__)
                   .parent
                   .resolve()).split("helpers")[0]

#ENV_FILE_TO_USE = current_path + '/.env.development'

# This variable could be set in a Dockerfile in order to
# check if we are in production or not.
try:
    os.environ['IN_PRODUCTION']
    ENV_FILE_TO_USE = current_path + '/.env.production'

except KeyError:
    ENV_FILE_TO_USE = current_path + '/.env.development'

load_dotenv(dotenv_path=ENV_FILE_TO_USE)

# ====== Production vs Development config ======
ISDEVELOPMENT = 2022

# ====== Backends paths ======

API_KEY_URL = "/apikeys"
REDIRECT_URL = "/redirect"
API_KEY_DOWN_URL = API_KEY_URL + "/down"
API_KEY_UP_URL = API_KEY_URL + "/up"
SERVICES_URL = "/services"
CHECK_URL = "/check"

SERVICES_HOST = os.getenv("SERVICES_HOST") + "/"

print("SERVICES_HOST: " + str(SERVICES_HOST))

JSON_HEADER = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
}

SHA_LEN = 64

RUN_MIGRATIONS = True

MSG_NO_AUTORIZADO = "No autorizado"
