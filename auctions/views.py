from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.core import serializers

from .models import User, Auction, Bid, Category, Comment, PersonalWatchlist
from .forms import AuctionForm


def index(request):
    auctions = Auction.objects.all()
    total_categories = Category.objects.all()
    user = request.user 
    if user.id is None:
        return render(request, "auctions/index.html")
    my_watchlist = PersonalWatchlist.objects.get(user=request.user)
    totalAuctions = my_watchlist.auctions.count()
    context = {
        'auctions': auctions,
        'categories': total_categories,
        'totalAuctions': totalAuctions,
        'my_watchlist': my_watchlist,
    }
    return render(request, "auctions/index.html", context)


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
            personal_watchlist = PersonalWatchlist.objects.create(user=user)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def add_auction(request):
    total_categories = Category.objects.all() 
    user = request.user
    if user.id is None:
        return render(request, "auctions/index.html")
    my_watchlist = PersonalWatchlist.objects.get(user=request.user)
    totalAuctions = my_watchlist.auctions.count()
    
    if request.method == 'GET':
        context = {
            'form': AuctionForm(),
            'categories': total_categories,
            'totalAuctions': totalAuctions,
        }

        return render(request, "auctions/add_auctions.html", context)
    else:
        form = AuctionForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']

            auctionCreated = Auction.objects.create(
                user=request.user,
                title=title, 
                description=description, 
                starting_bid=starting_bid,
            )
            
            return redirect('index')


def category_view(request, category):
    total_categories = Category.objects.all() 
    category_name = Category.objects.get(name=category)
    auctions = Auction.objects.filter(category=category_name)
    user = request.user
    if user.id is None:
        return render(request, "auctions/index.html")
    my_watchlist = PersonalWatchlist.objects.get(user=request.user)
    totalAuctions = my_watchlist.auctions.count()
    
    context = {
        'auctions': auctions,
        'categories': total_categories,
        'totalAuctions': totalAuctions,
        'category_name': category_name,
    }
    return render(request, "auctions/category.html", context)


def watchlist(request):
    total_categories = Category.objects.all() 
    if request.user.id is None:
        return redirect('index')

    my_watchlist = PersonalWatchlist.objects.get(user=request.user)
    totalAuctions = my_watchlist.auctions.count()
    context = {
        'categories': total_categories,
        'my_watchlist': my_watchlist,
        'totalAuctions': totalAuctions, 
    }
    return render(request, "auctions/watchlist.html", context)

def add_to_watchlist(request, auction):
    if request.method == 'POST':
        auction_to_add = Auction.objects.get(id=auction)
        watchlist = PersonalWatchlist.objects.get(user=request.user)
        watchlist.auctions.add(auction_to_add)
        watchlist.save()
        return HttpResponse('')

def bid_to_auction(request, auction):
    if request.method == 'POST':
        auction_to_add = Auction.objects.get(id=auction)
        total_bid = request.POST["totalBid"]
        bid = Bid.objects.create(user=request.user, auction=auction_to_add, bid=total_bid)
        auction_to_add.bids.add(bid)
        auction_to_add.last_bid = bid
        auction_to_add.save()
        return HttpResponse('success')

def auction_view(request, auction):
    if request.method == 'GET':
        if request.user.id is None:
            return redirect('index')

        total_categories = Category.objects.all() 
        my_watchlist = PersonalWatchlist.objects.get(user=request.user)
        totalAuctions = my_watchlist.auctions.count()
        auction = Auction.objects.get(id=auction)
        context = {
            'auction': auction,
            'categories': total_categories,
            'my_watchlist': my_watchlist,
            'totalAuctions': totalAuctions,

        }
        return render(request, 'auctions/auction_view.html', context)

def add_comment(request, auction):
    if request.method == 'POST':
        auction = Auction.objects.get(id=auction)
        comment = request.POST['comment']
        comment_object = Comment.objects.create(comment=comment, user=request.user)
        auction.comments.add(comment_object)
        auction.save()
        return HttpResponse('success')

def delete_auction_from_watchlist(request, auction):
    if request.method == 'POST':
        auction = Auction.objects.get(id=auction)
        my_watchlist = PersonalWatchlist.objects.get(user=request.user)
        my_watchlist.auctions.remove(auction)
        my_watchlist.save()
        return HttpResponse('success')


def delete_auction(request, auction):
    if request.method == 'GET':
        auction = Auction.objects.get(id=auction)
        if auction.user == request.user:
            auction.delete()
            return redirect('index')