import pymongo
import json

from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Credenziali e dettagli del cluster
username = "DataMan"
password = "Bicocca1"
clustername = "ClusterDataMan"
dbname = "Database"

# Connessione al cluster MongoDB
uri = "mongodb+srv://DataMan:Bicocca1@clusterdataman.f7nnvlh.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client[dbname]

# Nome della collezione in cui inserire il documento JSON
collection_name = "2022"

# Percorso del file JSON da caricare
json_file_path = "../Data Acquisition/Final_Data/FinalDataset2022.json"

# Caricamento del file JSON
with open(json_file_path) as file:
    data = json.load(file)

# Inserimento del documento JSON nella collezione
collection = db[collection_name]
insert_result = collection.insert_one(data)

# Verifica dell'inserimento
if insert_result.acknowledged:
    print("Il documento JSON con nome personalizzato è stato inserito correttamente.")
else:
    print("Si è verificato un errore durante l'inserimento del documento JSON.")

