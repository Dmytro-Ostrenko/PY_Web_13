from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .utils import get_mongodb


from django.contrib.auth.decorators import login_required
from mongoengine.errors import NotUniqueError

from bson import ObjectId


from .forms import AuthorForm, QuoteForm
from django.contrib import messages




@login_required
def add_quote(request):
    db = get_mongodb()
    authors_ = db.authors.find()
    collection = db.quotes
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            record = collection.insert_one(form.cleaned_data)
            tags = form.cleaned_data['tags'].split(',')
            [tag.strip() for tag in tags]
            choice_author = db.authors.find_one({"fullname": request.POST.get('author')})
            collection.update_one({"_id": ObjectId(record.inserted_id)},
                                  {"$set": {'author': choice_author['_id'], 'tags': tags}})

            return redirect('quotes:root')
        else:
            return render(request, 'quotes/add_quote.html', context={"authors": authors_, "form": form})

    return render(request, 'quotes/add_quote.html', context={"authors": authors_, "form": QuoteForm()})


@login_required
def add_author(request):
    db = get_mongodb()
    collection = db.authors
    if request.method == 'POST':

        form = AuthorForm(request.POST)
        if form.is_valid():
            authors = collection.find()
            if form.cleaned_data['fullname'] in [author['fullname'] for author in authors]:
                messages.error(request, f'Author {form.cleaned_data["fullname"]} already exists!')
                return redirect('quotes:add_author')
            collection.insert_one(form.cleaned_data)
            messages.success(request, f'Author {form.cleaned_data["fullname"]} added successfully')
            return redirect('quotes:add_author')

        else:
            return render(request, 'quotes/add_author.html', context={"form": form})

    return render(request, 'quotes/add_author.html', context={"form": AuthorForm()})


def show_tag(request, tag, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    quotes_show = [quote for quote in quotes if tag in quote['tags']]
    return render(request, 'quotes/tag.html',
                  context={"quotes": quotes_show, "tag": tag, "page": page})


def about_author(request, author_id):
    db = get_mongodb()
    author = db.authors.find_one({"_id": ObjectId(author_id)})

    return render(request, 'quotes/about.html', context={"author": author})






def main(request, page=1):
    db = get_mongodb()
    per_page = 10
    quotes = db.quotes.find()
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/index.html", context={'quotes': quotes_on_page})