from hashlib import sha256

def getSHAof(toHash):
    return sha256(toHash).hexdigest()    