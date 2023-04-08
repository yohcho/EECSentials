import pymongo

myclient = pymongo.MongoClient("mongodb+srv://yohcho:qw123edc@cluster0.ggonojo.mongodb.net/?retryWrites=true&w=majority")
db = myclient["EECSentials"]["Class"]

query = {"labels":{"$in":["introductory"]}}
example = db.find(query)

for result in example:
    print(result)