import pymongo

# Connect to MongoDB
try:
    mongos_dns = "ec2-52-42-104-41.us-west-2.compute.amazonaws.com"
    client = pymongo.MongoClient(mongos_dns)
    db = client["yelp"]
    business_collection = db["business"]
    user_collection = db["user"]
except Exception as e:
    print("Connection unsuccessful", e)


# collection = db["business"]
#
# docs = collection.find().limit(10)
# for doc in docs:
#     print(doc)


def test_read_collection(col: str) -> None:
    """
    Simple function to print 10 documents from a given collection
    :return:
    """
    collection = db[col]

    docs = collection.find().limit(10)
    for doc in docs:
        print(doc)


def create_business(b_id, name, addy, city, state, zip, lat, long,
                    stars) -> bool:
    """
    Create a new business and add it to the collection
    :return:
    """
    new_document = {
        "business_id": b_id,
        "name": name,
        "address": addy,
        "city": city,
        "state": state,
        "postal_code": zip,
        "latitude": lat,
        "longitude": long,
        "stars": stars,
        "review_count": 0,
        "is_open": 0,
        "attributes": {},
        "categories": "",
        "hours": None
    }
    business_collection.insert_one(new_document)
    result = business_collection.find_one({"business_id": b_id})
    print(result)
    return result == new_document


def find_biz_by_zip(zip_code: str) -> bool:
    """
    Find a Business by a given zip code
    Todo:
        Can we generalize this into a larger function that can decide
        to search by zip, state, or city?
    :param zip_code:
    :return:
    """
    result = business_collection.find_one({"business_id": zip_code})
    print(result)
    return result  # whether a result has been found


def find_all_biz_locations(name: str) -> bool:
    """
    Find all locations for a business given a name
    :param name:
    :return:
    """
    result = business_collection.find({"name": str})
    print([biz["zip"] for biz in result])
    return result



