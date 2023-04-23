import pymongo

client = pymongo.MongoClient("ec2-52-42-104-41.us-west-2.compute.amazonaws.com")
db = client["yelp"]
collection = db["business"]

def read_operations():
     
    """
    Various find ooperations on the collection
    :return:
    """
    print("\n")

    print("Philadelphia Businesses: ")
    philadelphia_businesses = collection.find({"city": "Philadelphia"})

    for business in philadelphia_businesses[:10]:
        print(business["name"])
    print("\n")

    print("Businesses in the Restaurants category: ")

    restaurant_businesses = collection.find({"categories": {"$regex": ".*Restaurants.*"}})

    for business in restaurant_businesses[:10]:
        print(business["name"])

    print("\n")

    print("Businesses with a rating of 4 or higher: ")

    high_rating_businesses = collection.find({"stars": {"$gte": 4}})

    for business in high_rating_businesses[:10]:
        print(business["name"])




def create_business(new_document) :
    """
    Create a new business and add it to the collection
    :return:
    """
    print("Inserting new document: ")

  
    result = collection.insert_one(new_document)
    print(result.inserted_id)
    print(collection.find_one({"_id": result.inserted_id}))
    



def update_operation(business_id):
    
    """
    Update a business from the collection
    :return:
    """
    restaurant_businesses= (collection.find_one({"business_id": business_id}))
    city = restaurant_businesses["city"]
    print("Updating business with id: ", business_id, "city: " , city)

    result = collection.update_one({"business_id": business_id}, {"$set": {"city": "New_city"}})
    print("Updated business with id: ", business_id, "new city:", collection.find_one({"business_id": business_id})['city'])
    print("Documents matched:", result.matched_count)
    print("Documents modified:", result.modified_count)

def remove_operation(business_id):

    """
    Remove a business from the collection
    :return:
    """
    print("Deleting the business with the id: ", business_id)
    result = collection.delete_one({"business_id": business_id})
    print("Documents deleted:", result.deleted_count)
    print("Deleted")
    print("Finding business with id: ", business_id)
    print(collection.find_one({"_id": business_id}))



new_business = {
    "name": "New Business",
    "address": {
        "street": "101 San Fernando",
        "city": "San Jose",
        "state": "CA",
        "zip": "95112"
    },
    "categories": ["New Category"],
    "stars": 4.1,
    "review_count": 3
}


business_id = "6444abb24bd62dabdc755ba3"

remove_operation("qkRM_2X51Yqxk3btlwAQIg")