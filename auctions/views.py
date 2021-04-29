from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Listing, Bid, Comment, CATEGORIES


def index(request):
    bids = Bid.objects.all()
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "bids": bids
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    current_price = get_price(listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_price": current_price,
        "comments": Comment.objects.all()
    })


# @login_required(login_url='auctions/login')
def add_comment(request, listing_id):
    user = request.user
    listing = listing_id
    use_listing = Listing.objects.get(id=listing)
    if request.method == "POST":
        if user.is_authenticated:
            try:
                query = request.POST['comment']
                if query:
                    comment = Comment.objects.create(created_by=user,content=query, rel_listing=use_listing)
                    comment.save()
            except Exception as e:
                print(e)
        else:
            messages.error(request, "You are not authenticated!")

    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id':listing,}))

def get_price(listing_id):
    current_price = Bid.objects.filter(listing_id=listing_id).last()
    if current_price is not None:
        return current_price.bid
    else:
        current_price = Listing.objects.get(id=listing_id).start_bid
        return current_price

def bid(request, listing_id):
    user = request.user
    listing = listing_id
    if request.method == "POST":
        bid = int(request.POST['bid'])
        get_starting_bid = Listing.objects.get(id=listing).start_bid
        print(get_starting_bid)
        if bid <= get_starting_bid:
            
            print("Please bet more money")
        else:
            current_price = get_price(listing_id)
            if current_price >= bid or current_price is None:
                messages.error(request, "You need to bet more to win this lot!")
            else:
                try:
                    new_bid = Bid.objects.create(listing_id=Listing.objects.get(id=listing),created_by=User.objects.get(username=user), start_bid=Listing.objects.get(id=listing).start_bid, bid=bid, )
                    new_bid.save()
                except Exception as e:
                    print(e)
    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id':listing,}))

def create(request):
    return render(request, "auctions/create.html")

def categories(request):
    categories = []
    for items in CATEGORIES:
        categories.append(list(items).pop())

    return render(request, 'auctions/categories.html', {
        "categories": categories
    })

def category(request, category):
    item_list = Listing.objects.filter(category=category)
    print(item_list)
    return render(request, 'auctions/category.html', {
        "item_list": item_list,
        "category": category
    })