from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.core import serializers

from .models import User, Auction, Bid, Category, Comment, PersonalWatchlist, Person
from .forms import AuctionForm


def index(request):
    auctions = Auction.objects.all().order_by('id').reverse()
    persons = Person.objects.all()
    user = request.user 
    if user.id is None:
        context = {
            'auctions': auctions,
            'persons': persons,
        }
        return render(request, "auctions/index.html", context)
    my_watchlist = PersonalWatchlist.objects.get(user=request.user)
    totalAuctions = my_watchlist.auctions.count()
    context = {
        'auctions': auctions,
        'totalAuctions': totalAuctions,
        'my_watchlist': my_watchlist,
        'persons': persons,
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
        if request.user.is_authenticated:
            return redirect('index')
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
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, "auctions/register.html")


def add_auction(request):
    persons = Person.objects.all()
    user = request.user
    if user.id is None:
        return redirect('login')
    my_watchlist = PersonalWatchlist.objects.get(user=request.user)
    totalAuctions = my_watchlist.auctions.count()
    
    if request.method == 'GET':
        context = {
            'form': AuctionForm(),
            'totalAuctions': totalAuctions,
            'persons': persons,
        }

        return render(request, "auctions/add_auctions.html", context)
    else:
        form = AuctionForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            category = form.cleaned_data['category']
            person = form.cleaned_data['person']
            image = form.cleaned_data['image']

            auctionCreated = Auction.objects.create(
                user=request.user,
                title=title, 
                description=description, 
                starting_bid=starting_bid,
                category=category,
                person=person,
                image=image,
            )
            
            return redirect('index')


def category_view(request, category, person):
    category_name = Category.objects.get(name=category)
    person_name = Person.objects.get(person=person)
    auctions = Auction.objects.filter(category=category_name, person=person_name).order_by('id').reverse()
    persons = Person.objects.all()
    user = request.user

    if user.id is None:
        return render(request, "auctions/index.html")
    my_watchlist = PersonalWatchlist.objects.get(user=request.user)
    totalAuctions = my_watchlist.auctions.count()
    
    context = {
        'auctions': auctions,
        'totalAuctions': totalAuctions,
        'category_name': category_name,
        'persons': persons,
    }
    return render(request, "auctions/category.html", context)

def my_listings(request, user):
    user_object = User.objects.get(username=user)
    auctions = Auction.objects.filter(user=user_object)
    my_watchlist = PersonalWatchlist.objects.get(user=request.user)
    totalAuctions = my_watchlist.auctions.count()

    if request.user.username != user:
        return redirect('my_listings', user=request.user.username)

    context = {
        'auctions': auctions,
        'my_watchlist': my_watchlist,
        'totalAuctions': totalAuctions,
    }

    return render(request, "auctions/my_listings.html", context)


def watchlist(request):
    persons = Person.objects.all()
    if request.user.id is None:
        return redirect('index')

    my_watchlist = PersonalWatchlist.objects.get(user=request.user)
    totalAuctions = my_watchlist.auctions.count()
    context = {
        'my_watchlist': my_watchlist,
        'persons': persons,
        'totalAuctions': totalAuctions, 
    }
    return render(request, "auctions/watchlist.html", context)

def add_to_watchlist(request, auction):
    if request.method == 'POST':
        auction_to_add = Auction.objects.get(id=auction)
        watchlist = PersonalWatchlist.objects.get(user=request.user)
        if auction_to_add in watchlist.auctions.all():
            watchlist.auctions.remove(auction_to_add)
            watchlist.save()
        else:
            watchlist.auctions.add(auction_to_add)
            watchlist.save()
        return HttpResponse('success')

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
        persons = Person.objects.all()

        if request.user.id is None:
            return redirect('login')

        my_watchlist = PersonalWatchlist.objects.get(user=request.user)
        totalAuctions = my_watchlist.auctions.count()
        auction = Auction.objects.get(id=auction)
        comments = auction.comments.all().order_by('id').reverse()
        context = {
            'auction': auction,
            'my_watchlist': my_watchlist,
            'persons': persons,
            'comments': comments,
            'totalAuctions':totalAuctions,
        }
        return render(request, 'auctions/auction_view.html', context)

def add_comment(request, auction):
    if request.method == 'POST':
        auction = Auction.objects.get(id=auction)
        comment = request.POST['comment']
        if not comment:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        comment_object = Comment.objects.create(comment=comment, user=request.user)
        auction.comments.add(comment_object)
        auction.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def delete_comment(request, comment):
    if request.method == 'POST':
        comment_object = Comment.objects.get(id=comment)
        comment_object.delete()
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

def close_listing(request, auction):
    if request.method == 'GET':
        auction_object = Auction.objects.get(id=auction)
        auction_object.closed = True
        auction_object.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
