from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_auction", views.add_auction, name="add_auction"),
    path("category/<str:category>", views.category_view, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_to_watchlist/<str:auction>", views.add_to_watchlist, name="add_to_watchlist"),
    path("bid_to_auction/<str:auction>", views.bid_to_auction, name="bid_to_auction"),
]
