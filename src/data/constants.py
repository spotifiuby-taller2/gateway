

# ====== Production vs Development config ====== 
ISDEVELOPMENT = 2022

# ====== Backends paths ====== 

API_KEY_URL = "/apikeys"
REDIRECT_URL = "/redirect"
API_KEY_DOWN_URL = API_KEY_URL + "/down"
API_KEY_UP_URL = API_KEY_URL + "/up"
SERVICES_URL = "/services"


SHA_LEN = 64
DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@localhost:5432/apikeys'


