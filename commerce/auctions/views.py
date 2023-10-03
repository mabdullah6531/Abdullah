from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *


def index(request):
    data = YourModel.objects.filter(closed = False)
    return render(request, 'auctions/index.html', {'data': data})


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

def addlisting(request):
    if request.method == "POST":
        title = request.POST.get("title")
        bid = request.POST.get("bid")
        category = request.POST.get("category")
        description = request.POST.get("Description")
        image_url = request.POST.get("Image")
        price = bids(price = bid, highest_bidder = request.user)
        price.save()
        # response = requests.get(image_url)
        # if response.status_code == 200:
        #     image_content = response.content
        #     image_name = image_url.split('/')[-1]
        #     image_content = ContentFile(response.content, name=image_name)
        your_model = YourModel(title=title, bid=price, category=category, image=image_url, description=description, user = request.user)
            # your_model.image.save(image_name, ContentFile(image_content))
        your_model.save()
        return HttpResponseRedirect(reverse("index"),{
            "message": "Request Generated"
        })
    return render(request, "auctions/listing.html")

def listings(request,id):
    data = YourModel.objects.get(id = id)
    comments_obj = comments.objects.filter(yourmodel = data)
    if request.user.is_authenticated:
        if not watchlist.objects.filter(yourmodel = data, user = request.user).exists():
            exist = False
        elif watchlist.objects.filter(yourmodel = data, user = request.user).exists():
            exist = True
        
        if data.user == request.user:
            candelete = 1
        else:
            candelete = 0
        
        return render(request, "auctions/active.html",{
            "data": data,
            "authen": "1",
            "comments_obj": comments_obj,
            "exist": exist,
            "candelete": candelete
        })
    else:
        return render(request, "auctions/active.html",{
            "data": data,
            "authen": "0",
            "comments_obj": comments_obj
        })

def new_bid(request,id):
    if request.method == "POST":
        data = YourModel.objects.get(id = id)
        new_bid = int(request.POST.get('new_bid'))
        if new_bid > data.bid.price:
            data.bid.price = new_bid
            data.bid.highest_bidder = request.user
            data.bid.save()
        comments_obj = comments.objects.filter(yourmodel = data)
        if request.user.is_authenticated:
            if not watchlist.objects.filter(yourmodel = data, user = request.user).exists():
                exist = False
            elif watchlist.objects.filter(yourmodel = data, user = request.user).exists():
                exist = True
            
            if data.user == request.user:
                candelete = 1
            else:
                candelete = 0
            
            return render(request, "auctions/active.html",{
                "data": data,
                "authen": "1",
                "comments_obj": comments_obj,
                "exist": exist,
                "candelete": candelete
            })
        else:
            return render(request, "auctions/active.html",{
                "data": data,
                "authen": "0",
                "comments_obj": comments_obj
            })
        # new_bid = int(request.POST.get('new_bid'))
        # if new_bid > data.bid.price:
        #     data.bid.price = new_bid
        #     data.bid.highest_bidder = request.user
        #     data.bid.save()
    return HttpResponseRedirect(reverse("index"))

def comment(request, id):
    if request.method == "POST":
        data = YourModel.objects.get(id = id)
        comment = request.POST.get("comment")
        tosave = comments(yourmodel= data, user = request.user, message = comment)
        tosave.save()
        if not watchlist.objects.filter(yourmodel = data, user = request.user).exists():
                exist = False
        elif watchlist.objects.filter(yourmodel = data, user = request.user).exists():
            exist = True
        
        if data.user == request.user:
            candelete = 1
        else:
            candelete = 0
        comments_obj = comments.objects.filter(yourmodel = data)
        return render (request, "auctions/active.html",{
            "data": data,
            "authen": "1",
            "comments_obj": comments_obj,
            "exist": exist,
            "candelete": candelete
        })


def watchlists(request,id):
    if request.method == "POST":
        data = YourModel.objects.get(id = id)
        tosave = watchlist(yourmodel = data, user = request.user)
        tosave.save()
        watchlist_items = watchlist.objects.filter(user=request.user)
        yourmodel_objects = [item.yourmodel for item in watchlist_items]
        return render(request, "auctions/watchlist.html",{
            "watchlist_items": watchlist_items,
            "yourmodel_objects": yourmodel_objects
        })
    watchlist_items = watchlist.objects.filter(user=request.user)
    yourmodel_objects = [item.yourmodel for item in watchlist_items]
    return render(request, "auctions/watchlist.html",{
        "watchlist_items": watchlist_items,
        "yourmodel_objects": yourmodel_objects
    })

def remove(request, id):
    if request.method == "POST":
        data = YourModel.objects.get(id = id)
        remove_listing = watchlist.objects.get(yourmodel = data ,user=request.user)
        remove_listing.delete()
        return HttpResponseRedirect(reverse("index"))


def close_listing(request, id):
    if request.method == "POST":
        store = YourModel.objects.get(id = id)
        remove_listing = watchlist.objects.filter(yourmodel = store)
        remove_listing.delete()
        store.closed = True
        store.save()
        data = auctionswon(title = store.title, bid = store.bid, image = store.image, category = store.category, description = store.description)
        data.save()
    
    won = auctionswon.objects.all()
    return render (request, "auctions/active.html",{
        "data": data
    })

def closed(request):
    won = auctionswon.objects.all()
    return render (request, "auctions/auctionswon.html",{
        "won": won
    })


def category(request):
    categories = ["None", "Fashion", "Toys", "Electronics", "Home Appliences", "Pets", "Bikes", "Cars", "Clothings", "Antique", "Furniture"]
    return render (request, "auctions/categories.html",{
        "categories": categories
    })

def fetch(request, title):
    data = YourModel.objects.filter(category = title, closed = False)
    return render (request, "auctions/index.html",{
        "data": data
    })