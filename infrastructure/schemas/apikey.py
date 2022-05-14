def apikeyEntity(item) -> dict:
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
