#from asyncio.log import logger
import hashlib
import string
import random
import logging
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

    print("destinyHost: " + destinyHost[:endIndex])
    return destinyHost[:endIndex]


def getMethodFrom(redirectTo):
    firstColon = redirectTo.index(":")
    firstSlash = redirectTo[firstColon:].index("/")
    firstQuestionMark = redirectTo[firstSlash:].index("?")
    if firstQuestionMark < 0:
        secondSlash = redirectTo[firstSlash:].index("/")
        return redirectTo[secondSlash + 1:]

    return "services"
