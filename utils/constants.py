import os
from dotenv import load_dotenv

load_dotenv()

# ====== Production vs Development config ======
ISDEVELOPMENT = 2022

# ====== Backends paths ======

API_KEY_URL = "/apikeys"
REDIRECT_URL = "/redirect"
API_KEY_DOWN_URL = API_KEY_URL + "/down"
API_KEY_UP_URL = API_KEY_URL + "/up"
SERVICES_URL = "/apikeys/services"

SERVICES_HOST = os.getenv("SERVICES_HOST") + "/"

JSON_HEADER = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
}

SHA_LEN = 64
