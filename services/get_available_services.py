from infrastructure.db.database import current_connection


def getAvailableServicesFromDB():
    availableServices = list(current_connection.find({}))
    #availableServices = availableServices[1:]
    contador = 0
    for service in availableServices:
        del service['_id']
        service['id'] = contador
        contador = contador + 1
    return availableServices
