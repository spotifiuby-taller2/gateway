# from asyncio.log import logger
import hashlib
import string
import random
import logging
import os

logging.basicConfig(level=logging.DEBUG)


def get_new_api_key():
    h = hashlib.new('sha256')
    secret_str = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=20))
    logging.debug(secret_str)
    h.update((secret_str).encode('utf8'))
    return h.hexdigest()


aux = get_new_api_key()[:20]
logging.debug("new apikey: " + aux)


def getHostFrom(url):
    startIndex = url.index("//") + 2
    destinyHost = url[startIndex:]
    endIndex = destinyHost.index("/")

    if endIndex == -1:
        return destinyHost

    return destinyHost[:endIndex]


def getMethodFrom(redirectTo):
    firstColon = redirectTo.index(":")
    subRedirectToFirstColon = redirectTo[firstColon + 1:]

    try:
        secondColon = subRedirectToFirstColon.index(":")
        subRedirectToSecondColon = subRedirectToFirstColon[secondColon:]
    except Exception as e:
        # Production
        reference = subRedirectToFirstColon.index("appgateway.herokuapp.com")
        subRedirectToSecondColon = subRedirectToFirstColon[reference:]

    firstSlash = subRedirectToSecondColon.index("/")

    if "services" not in subRedirectToSecondColon:
        secondSlash = subRedirectToSecondColon.index("/")
        subRedirectTo = subRedirectToSecondColon[secondSlash:]

    else:
        firstQuestionMark = subRedirectToSecondColon.index("?")
        subRedirectTo = subRedirectToSecondColon[firstSlash +
                                                 1:firstQuestionMark]

    return subRedirectTo


def is_production():
    try:
        os.environ['IN_PRODUCTION']
        return True

    except KeyError:
        return False
