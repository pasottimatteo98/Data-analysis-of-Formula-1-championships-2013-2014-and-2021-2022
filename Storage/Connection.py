import pymongo
import json

# Credenziali e dettagli del cluster
username = "DataMan"
password = "Bicocca1"
clustername = "ClusterDataMan"
dbname = "Database"
collection_name = "Data"

# Connessione al cluster MongoDB
uri = f"mongodb+srv://{username}:{password}@{clustername}.f7nnvlh.mongodb.net/{dbname}?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)

# Accesso alla collezione
db = client[dbname]
collection = db[collection_name]


#Esempio
query = {"Fernando Alonso": {"$exists": True}}
cursor = collection.find(query)

for document in cursor:
    print(document["Fernando Alonso"])

# Chiudi la connessione
client.close()
