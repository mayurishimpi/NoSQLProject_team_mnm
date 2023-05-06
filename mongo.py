import heapq

import pymongo

# Connect to MongoDB
try:
    # Good
    mongos_dns = "mongodb://ec2-52-44-206-90.compute-1.amazonaws.com:27017/?tls=false"

    # Not Good
    # mongos_dns = "ec2-54-90-251-174.compute-1.amazonaws.com"
    client = pymongo.MongoClient(mongos_dns)
    db = client["yelp"]
    business_collection = db["business"]
    user_collection = db["user"]
    review_collection = db["review"]

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

    docs = collection.find().limit(1)
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


def update_biz(b_id, name, addy, city, state, zip, lat, long,
               stars) -> bool:
    new_document = {
        "$set": {
            "name": name,
            "address": addy,
            "city": city,
            "state": state,
            "postal_code": zip,
            "latitude": lat,
            "longitude": long,
            "stars": stars
        }
    }
    business_collection.update_one({"business_id": b_id}, new_document)
    res = business_collection.find_one({"business_id": b_id})
    print(res)
    return True


# update_biz("afu3nfdovijw4r", "Mickey's Barbershop", "221B Baker Street", "Worcester", "UK", "34514", "300", "100", "3")
# update_biz("afu3nfdovijw4r", "Mickey's Barbershop", "221B Baker Street", "London", "UK", "34514", "200", "300", "4")

def find_biz_by_zip(zip_code: str) -> None:
    """
    Find a Business by a given zip code
    Todo:
        Can we generalize this into a larger function that can decide
        to search by zip, state, or city?
    :param zip_code:
    :return:
    """
    result = business_collection.find({"postal_code": zip_code}).limit(10)
    print([biz for biz in result])


def find_all_biz_locations(name: str) -> bool:
    """
    Find all locations for a business given a name
    :param name:
    :return:
    """
    result = business_collection.find({"name": name})
    print([biz["postal_code"] for biz in result])
    return result


# Todo: Can we speed this query up by passing in some arguments into the find function?
def find_biz_by_street(street: str) -> bool:
    for biz in business_collection.find():
        if street in biz['address']:
            print(biz)


def find_biz_by_category(category: str) -> bool:
    for biz in business_collection.find().limit(500):
        if biz["categories"] and category in biz["categories"]:
            print(biz)


def find_k_highest_rated_biz(k: int) -> list:
    def rating(b) -> int:
        return -1 * b["stars"] * b["review_count"]

    # def find_biz_by_id(id: str):
    #     print(business_collection.find_one({"business_id": id}))

    h = []

    for biz in business_collection.find().limit(500):
        if len(h) < k:
            heapq.heappush(h, (rating(biz), biz["business_id"]))
        else:
            heapq.heappushpop(h, (rating(biz), biz["business_id"]))

    for tup in h:
        print(business_collection.find_one({"business_id": tup[1]}))

    return h


def find_k_most_reviewed_biz(k: int) -> list:
    h = []

    for biz in business_collection.find().limit(500):
        if len(h) < k:
            heapq.heappush(h, (biz["review_count"], biz["business_id"]))
        else:
            heapq.heappushpop(h, (biz["review_count"], biz["business_id"]))

    for tup in h:
        print(business_collection.find_one({"business_id": tup[1]}))

    return h


def find_k_highest_rated_users(k: int) -> list:
    """
    Find the k users with the highest ratings.

    Args:
        k (int): The number of top-rated users to find.

    Returns:
        list: A list of tuples, each containing a user's rating and user ID.
    """

    def calculate_user_rating(user_data: dict) -> int:
        """
        Calculate a user's rating based on their "useful", "cool", and "funny" fields.

        Args:
            user_data (dict): A dictionary representing a user's data.

        Returns:
            int: The user's rating.
        """
        rating = -1 * user_data["useful"] + user_data["cool"] + user_data[
            "funny"] + user_data["review_count"]
        return rating

    # Initialize a list to hold the k highest rated users.
    highest_rated_users = []

    # Iterate through the first 50 users in the user collection.
    for user in user_collection.find().limit(50):
        user_rating = calculate_user_rating(user)

        # Use a heap to keep track of the k highest rated users seen so far.
        if len(highest_rated_users) < k:
            heapq.heappush(highest_rated_users, (user_rating, user["user_id"]))
        else:
            heapq.heappushpop(highest_rated_users,
                              (user_rating, user["user_id"]))

    # Print each of the k highest rated users and return the list of tuples.
    for user_rating, user_id in highest_rated_users:
        highest_rated_user = user_collection.find_one({"user_id": user_id})
        print(highest_rated_user)

    return highest_rated_users


def find_k_newest_yelping_users(k: int) -> list:
    """
    Find the k users with the highest ratings.

    Args:
        k (int): The number of top-rated users to find.

    Returns:
        list: A list of tuples, each containing a user's rating and user ID.
    """

    # Initialize a list to hold the k highest rated users.
    newest_users = []

    # Iterate through the first 50 users in the user collection.
    for user in user_collection.find().limit(500):

        # Use a heap to keep track of the k highest rated users seen so far.
        if len(newest_users) < k:
            heapq.heappush(newest_users,
                           (user["yelping_since"], user["user_id"]))

        else:
            heapq.heappushpop(newest_users,
                              (user["yelping_since"], user["user_id"]))

    # Print each of the k highest rated users and return the list of tuples.
    for user_rating, user_id in newest_users:
        highest_rated_user = user_collection.find_one({"user_id": user_id})
        print(highest_rated_user)

    return newest_users


def find_reviews_for_biz(name: str):
    biz = business_collection.find_one({"name": name})

    reviews = review_collection.find(
        {"business_id": biz["business_id"]}).limit(10)
    for r in reviews:
        print(r)


def find_reviews_by_zip(zip: str):
    biz_in_zip = business_collection.find({"postal_code": zip})
    biz_ids = [b["business_id"] for b in biz_in_zip]

    for r in review_collection.find().limit(1000):
        if r["business_id"] in biz_ids:
            print(r)


def find_reviews_by_category(category: str):
    biz_ids = []
    for biz in business_collection.find().limit(500):
        if biz["categories"] and category in biz["categories"]:
            biz_ids.append(biz["business_id"])

    print(biz_ids)

    for r in review_collection.find().limit(10000):
        if r["business_id"] in biz_ids:
            print(r)


def find_reviews_by_user_name(name: str):
    user = user_collection.find_one({"name": name})
    u_id = user["user_id"]
    # print(user)

    # for review in review_collection.find():
    #     if review["user_id"] == user_id:
    #         print(review)
    for review in review_collection.find({"user_id": u_id}):
        print(review)

