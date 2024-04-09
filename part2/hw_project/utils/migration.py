import os
import django

from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw_project.settings")
django.setup()

from quotes.models import Quote, Tag, Author



client = MongoClient("mongodb://localhost")
db = client.djangohw

authors = db.authors.find()


for author in authors:
    author_data = {
        'fullname': author['fullname'],
        'born_date': author['born_date'],
        'born_location': author['born_location'],
    }
    if 'description' in author:
        author_data['description'] = author['description']
    Author.objects.get_or_create(**author_data)


quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote['tags']:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exist_quote = bool(len(Quote.objects.filter(quote=quote['quote'])))
    if not exist_quote:
        author = db.authors.find_one({"_id": quote['author']})
        a = Author.objects.get(fullname=author['fullname'])
        q = Quote.objects.create(
            quote=quote['quote'],
            author=a
        )
        for tag in tags:
            q.tags.add(tag)