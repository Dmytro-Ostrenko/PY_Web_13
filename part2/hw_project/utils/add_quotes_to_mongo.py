import json
from bson import ObjectId
from pymongo import MongoClient


# Підключення до MongoDB по localhost
client = MongoClient("mongodb://localhost")
db = client.djangohw

with open('quotes.json', 'r', encoding='utf-8') as fd:
    quotes = json.load(fd)

for quote in quotes:

    author = db.authors.find_one({'fullname': quote['author']})

    if author:
        db.quotes.insert_one({
            'quote': quote['quote'],
            'tags': quote['tags'],
            'author': ObjectId(author['_id'])
        })
