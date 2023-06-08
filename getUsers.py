from pymongo import MongoClient

def getUsers(date, mongo_db_uri):
    # Conexion a Mongo y obtener base de datos y colleciones
    client = MongoClient(mongo_db_uri)
    db = client["Users"]
    assistantCollection = db["Assistant"]
    usersCollection = db["users"]

    # Obtener las macAddress de los usuarios conectados en fecha especifica
    macAddress = assistantCollection.find_one({"date": date})

    # Eliminamos datos que no queremos usar
    del macAddress["_id"]
    del macAddress["_gateway"]
    del macAddress["picoTunnel"]

    # Creamos un arreglo de las macAddress unicamente
    arrMacAddress = list(macAddress.values())

    # Creamos un arreglo de la informacion de los usuarios que corresponden a la macAddress
    usuarios = list(usersCollection.find({'Addres': {'$in': arrMacAddress}}))

    return usuarios

