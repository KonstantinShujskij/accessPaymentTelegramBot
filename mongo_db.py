import pymongo
from utils import Struct
from data import config

client = pymongo.MongoClient(f'mongodb+srv://{config.MONGO_LOGIN}@cluster0.qskh6cd.mongodb.net/?retryWrites=true&w=majority')

db = client.test
coll = db.partners


def create_new_partner(telegram_id):
    coll.insert_one({
        'telegram': telegram_id,
        'api': 'undefined',
        'status': 'create'
    })


def ban_partner(telegram_id):
    partner = coll.find_one({"telegram": telegram_id}, {"_id": 0})
    query = {'$set': {"status": 'ban'}}
    coll.update_one(partner, query)


def reban_partner(telegram_id):
    partner = coll.find_one({"telegram": telegram_id}, {"_id": 0})
    query = {'$set': {"status": 'allow'}}
    coll.update_one(partner, query)


def wait_partner(telegram_id):
    partner = coll.find_one({"telegram": telegram_id}, {"_id": 0})
    query = {'$set': {"status": 'check'}}
    coll.update_one(partner, query)


def refresh_partner(telegram_id):
    partner = coll.find_one({"telegram": telegram_id}, {"_id": 0})
    query = {'$set': {"status": 'allow'}}
    coll.update_one(partner, query)


def allow_partner(telegram_id, access_id):
    partner = coll.find_one({"telegram": telegram_id}, {"_id": 0})
    query = {'$set': {"status": 'allow', 'api': access_id}}
    coll.update_one(partner, query)


def clear_partner(telegram_id):
    coll.delete_one({"telegram": telegram_id})


def get_partner(telegram_id):
    partner = coll.find_one({"telegram": telegram_id}, {"_id": 0})

    if not partner:
        return None

    return Struct(**partner)


create_new_partner('122')
allow_partner('122', 89988998)



