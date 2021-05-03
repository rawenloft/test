from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Listing, Bid, Comment, CATEGORIES, Watchlist


def index(request):
    user = request.user
    listing = Listing.objects.all()
    update_price(listing)
    if user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=user)
    else:
        watchlist = ''
    return render(request, "auctions/index.html", {
        "listings": listing,
        "watchlist": watchlist,
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

def check_watchlist(username, listing_id):
    user = username
    watchlist = Watchlist.objects.filter(user=user)
    if watchlist:
        for item in watchlist:
            if item.user == user:
                return True
    return False

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    current_price = get_price(listing_id)
    bids = Bid.objects.filter(listing_id=listing_id)
    username = request.user
    if username.is_authenticated:
        watchlist = Watchlist.objects.filter(user=username)
        watched = Watchlist.objects.filter(user=username, listing=listing).exists()
    else: 
        watchlist = ""
        watched = ""

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_price": current_price,
        "comments": Comment.objects.all(),
        "bids": bids,
        "watched": watched,
        "watchlist": watchlist,
    })



@login_required(login_url='login')
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
                else:
                    messages.error(request, "Comment should not be empty!")
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

def update_price(listing):
    for item in listing:
        item_price = get_price(item.id)
        current_price = Listing.objects.filter(id=item.id).update(current_price=item_price)
        item.refresh_from_db()
    

@login_required(login_url='login')
def bid(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    bids = Bid.objects.filter(listing_id=listing_id)
    if user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=user)
        watched = Watchlist.objects.filter(user=user, listing=listing).exists()
    else: 
        watchlist = ""
        watched = ""
    if request.method == "POST":
        bid = int(request.POST['bid'] or 0)
        get_starting_bid = Listing.objects.get(id=listing_id).start_bid
        current_price = get_price(listing_id)
        new_price = Listing.objects.filter(id=listing_id).update(current_price=current_price)
        listing.refresh_from_db()
        if bid <= current_price:
            return render(request,'auctions/listing.html', {
                "listing": listing,
                "current_price": listing.current_price,
                "message": "Your bet should be bigger than current price! Please bet more money!",
                "bids": bids,
                "watched": watched,
                "watchlist": watchlist,
            })
        try:
            if listing.created_by == user:
                return render(request,'auctions/listing.html', {
                    "listing": listing,
                    "current_price": listing.current_price,
                    "message": "You can not bet on your own listing.",
                    "bids": bids,
                    "watched": watched,
                    "watchlist": watchlist,
                }) 
            new_bid = Bid.objects.create(listing_id=listing,created_by=request.user, start_bid=listing.start_bid, bid=bid, )
            new_bid.save()
        except Exception as e:
            print(e)
    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id':listing.id,}))

def create_listing(request):
    user = request.user
    if request.method == "POST":
        title = request.POST["title"]
        category = request.POST["category"]
        description = request.POST["description"] or ""
        img_url = request.POST["img_url"] or "https://st4.depositphotos.com/14953852/22772/v/450/depositphotos_227725020-stock-illustration-image-available-icon-flat-vector.jpg"
        start_bid = request.POST["start_bid"]
        try:
            listing = Listing.objects.create(created_by=user, title=title, category=category, description=description, img_url=img_url, start_bid=start_bid,created_at=True, active=True,)
            listing.save()
            return render(request, "auctions/listing.html", {
                "listing":listing,
                "current_price": get_price(listing.id),
            })
        except Exception as e:
            print(e)
    return render(request, "auctions/create.html")

def categories(request):
    user = request.user
    if user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=user)
    else:
        watchlist = ""
    categories = []
    for items in CATEGORIES:
        categories.append(list(items).pop())

    return render(request, 'auctions/categories.html', {
        "categories": categories,
        "watchlist": watchlist,
    })

def category(request, category):
    user = request.user
    if user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=user)
    else:
        watchlist = ""
    listing = Listing.objects.filter(category=category)
    if not listing:
        message = "No items selling for now. Please come back later."
    else:
        message = ''
    update_price(listing)
    return render(request, 'auctions/category.html', {
        "item_list": listing,
        "category": category,
        "message": message,
        "watchlist": watchlist,
    })

@login_required(login_url='login')
def add_to_watch(request,listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    watch_item = Watchlist.objects.filter(user=user, listing=listing)
    if watch_item:
        Watchlist.objects.filter(user=user,listing=listing).delete()
    else:
        watchlist = Watchlist(user=user, listing=listing)
        watchlist.save()
    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id':listing.id,}))


def watchlist(request, user_username):
    user = request.user
    watchlist = Watchlist.objects.filter(user=user)
    if not watchlist:
        message = "No items for watching."
        print(watchlist)
    else:
        message = ""
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        "message": message,
    })

def close_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if listing.active:
        deactivate = Listing.objects.filter(id=listing_id).update(active=False)
    else:
        deactivate = Listing.objects.filter(id=listing_id).update(active=True)
    listing.refresh_from_db()
    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id':listing_id,}))

