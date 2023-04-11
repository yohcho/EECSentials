import pymongo
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb+srv://yohcho:qw123edc@cluster0.ggonojo.mongodb.net/?retryWrites=true&w=majority")
db = myclient["EECSentials"]["Class"]
dbSession = myclient["EECSentials"]["Session"]

val = dbSession.find_one({"_id":ObjectId("6435289e930f12ba4e613f58")})
print(val)


"6435289e930f12ba4e613f58"