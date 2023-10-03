from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addlisting", views.addlisting, name="addlisting"),
    path("<int:id>/listings", views.listings, name="listings"),
    path("<int:id>/bid", views.new_bid, name="bid"),
    path("<int:id>/comment", views.comment, name="comment"),
    path("<int:id>/watchlist", views.watchlists, name="watchlist"),
    path("<int:id>/remove", views.remove, name="remove"),
    path("<int:id>/close", views.close_listing, name="delete"),
    path("closed", views.closed, name="closed"),
    path("category", views.category, name="category"),
    path("<str:title>/fetch", views.fetch, name="fetch"),
]