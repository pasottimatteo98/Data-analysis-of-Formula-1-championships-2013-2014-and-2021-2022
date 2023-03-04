import pymongo


username = "DataMan"
password = "Bicocca1"
clustername = "ClusterDataMan"
dbname = "Data"

client = pymongo.MongoClient("mongodb+srv://DataMan:" + password + "@" + clustername + ".f7nnvlh.mongodb.net/?retryWrites=true&w=majority")
db = client.test

db = client[dbname]
col = db["Spacelink_Satellites"]
result = client[dbname]["Spacelink_Satellites"].find()
for i in result:

    print(i)

