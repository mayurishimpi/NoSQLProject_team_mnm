import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("ec2-52-42-104-41.us-west-2.compute.amazonaws.com")
db = client["yelp"]
collection = db["business"]

# Query for documents
docs = collection.find().limit(10)
for doc in docs:
    print(doc)
