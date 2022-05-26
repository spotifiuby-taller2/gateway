def apikeyEntity(item) -> dict:
    '''
    print(item["_id"])
    print(item["apikey"])
    print(item["name"])
    print(item["active"])
    print(item["creation_date"])
    print(item["description"])
    '''
    return {
        "id": str(item["_id"]),
        "apiKey": item["apiKey"],
        "name": item["name"],
        "active": item["active"],
        "creationDate": item["creationDate"],
        "description": item["description"]
    }


def apikeysEntity(items) -> list:
    return [apikeyEntity(item) for item in items]
