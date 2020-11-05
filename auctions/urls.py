from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_auction", views.add_auction, name="add_auction"),
    path("category/<str:person>/<str:category>", views.category_view, name="category"),
    path("my_listings/<str:user>", views.my_listings, name="my_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_to_watchlist/<str:auction>", views.add_to_watchlist, name="add_to_watchlist"),
    path("bid_to_auction/<str:auction>", views.bid_to_auction, name="bid_to_auction"),
    path("auction/<str:auction>", views.auction_view, name="auction_view"),
    path("add_comment/<str:auction>", views.add_comment, name="add_comment"),
    path("delete_comment/<str:comment>", views.delete_comment, name="delete_comment"),
    path("delete_auction_from_watchlist/<str:auction>", views.delete_auction_from_watchlist, name="delete_auction_from_watchlist"),
    path("delete_auction/<str:auction>", views.delete_auction, name="delete_auction"),
    path("close_listing/<str:auction>", views.close_listing, name="close_listing"),
]
