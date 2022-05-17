def apikeyEntity(item) -> dict:
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4")
    print(item["_id"])
    print(item["apikey"])
    print(item["name"])
    print(item["active"])
    print(item["creation_date"])
    print(item["description"])

    return {
        "id": str(item["_id"]),
        "apikey": item["apikey"],
        "name": item["name"],
        "active": item["active"],
        "creation_date": item["creation_date"],
        "description": item["description"]
    }


def apikeysEntity(items) -> list:
    return [apikeyEntity(item) for item in items]
