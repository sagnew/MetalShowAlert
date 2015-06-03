import pymongo

# Connection to Mongo DB
conn = pymongo.MongoClient()

db = conn.numbers
users = db.users

def insert(number, city):
    users.insert({'number': number, 'city': city})

def get_user_by_number(number):
    return users.find_one({'number': number})

def get_users_by_city(city):
    return users.find({'city': city})

def update_user(number, city):
    user = get_user_by_number(number)
    updated_user = {'number': number, 'city': city}
    users.update({'_id': user['_id']}, {"$set": updated_user}, upsert=False)
