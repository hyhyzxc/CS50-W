from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.filter(closed = False)
    return render(request, "auctions/index.html",{
        "listings": listings
    })
  

@login_required
def create(request):
    if request.method == "POST":
        name = str(request.POST['name'])
        description = request.POST['description']
        price = float(request.POST['price'])
        image = request.POST['image']
        category = request.POST['category']
        lister = request.user
        new_list = Listing(name=name, description = description, price=price, image=image, category=category, lister=lister)
        new_list.save()
        new_bid = Bid(listing = new_list, bidder = lister, bid_price = price)
        new_bid.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")

@login_required
def listing(request, listing_id):
    if request.method == "GET":
        listing = Listing.objects.get(id = listing_id)
        bids = Bid.objects.filter(listing = listing)
        comments = Comment.objects.filter(item = listing)
        winning_bid = Bid.objects.get(bid_price = listing.price)
        watchlists = request.user.watchlists.all()
        if listing.closed == True:
            message = "Bid Closed!"
            winner = winning_bid.bidder
        else:
            message = None
            winner = None
       
        return render(request, "auctions/listing.html", {
            "listing" : listing,
            "bids" : bids,
            "comments": comments,
            "num_bids":bids.count(),
            "message" : message,
            "winner" : winner,
            "watchlists" : watchlists
        })
    else:
        
        listing = Listing.objects.get(id = listing_id)
        user = request.user
        if 'watchlist' in request.POST:
            user.watchlists.add(listing)
           
        if 'unwatchlist' in request.POST:
            user.watchlists.remove(listing)
            
        try:
            bid_price = float(request.POST["bid_price"])
        except:
            bid_price = None
        try:
            comment = request.POST["comment"]
        except:
            comment = None
        bids = Bid.objects.filter(listing = listing)
        comments = Comment.objects.filter(pk = listing_id)
        if user == listing.lister:
            try:
                winning_bid = Bid.objects.get(bid_price = listing.price)
            except:
                winning_bid = None
            listing.closed = True
            listing.save()
            return render(request, "auctions/listing.html", {
            "listing" : listing,
            "bids" : bids,
            "comments": comments,
            "num_bids":bids.count(),
            "message": "Bid closed!",
            "winner" : winning_bid.bidder
        })
        
        if bid_price != None and bid_price < listing.price:
            return render(request, "auctions/listing.html", {
            "listing" : listing,
            "bids" : bids,
            "comments": comments,
            "num_bids":bids.count(),
            "message": "Bid price too low."
        })
        new_bid = Bid(listing = listing, bidder = user, bid_price = bid_price)
        if bid_price != None:
            new_bid.save()
            listing.price = new_bid.bid_price
            listing.save()
        if comment != None:
            new_comment = Comment(commenter = user, comment = comment, item = listing)
            new_comment.save()
        return HttpResponseRedirect(reverse("index"))

@login_required
def watchlist(request):
    user = request.user
    listings = user.watchlists.all()
    list_closed = Listing.objects.filter(closed = True)
    for list in list_closed:
        if list not in listings:
            list.delete()
    return render(request, "auctions/watchlist.html",{
        "listings": listings
    })

@login_required
def category(request):
    categories = Listing.objects.values_list('category', flat = True).distinct()
    return render(request, "auctions/category.html", {
        "categories" : categories
    })
    
@login_required
def show_category(request, listing_category):
    listings = Listing.objects.filter(category = listing_category)
    return render(request, "auctions/show_cat.html" ,{
        "listings" : listings,
        "category" : listing_category
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
