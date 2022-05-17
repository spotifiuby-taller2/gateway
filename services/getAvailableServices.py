from infrastructure.db.database import current_connection


def getAvailableServicesFromDB():
    availableServices = list(current_connection.find({}))
    availableServices = availableServices[1:]
    for service in availableServices:
        del service['_id']
    return availableServices
