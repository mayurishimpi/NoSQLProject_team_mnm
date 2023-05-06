# Requires the PyMongo package.
# https://api.mongodb.com/python/current

'''
I'm gonna just throw a bunch of queries that I use from compass into here!
'''

from pymongo import MongoClient

#Narinder Server (should be working)
client = MongoClient("mongodb://ec2-52-44-206-90.compute-1.amazonaws.com:27017/?tls=false")


#Not good, badd
# client = MongoClient('mongodb://ec2-54-90-251-174.compute-1.amazonaws.com:27017/')

filter={
    'state': 'CA'
}

result = client['yelp']['business'].find(
  filter=filter
)
for doc in result:
    print(doc)
