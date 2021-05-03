from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path('listing/<int:listing_id>', views.listing, name="listing"),
    path('create', views.create_listing, name="create"),
    path('categories', views.categories, name="categories"),
    path('categories/<str:category>', views.category, name="category"),
    path('<int:listing_id>', views.add_comment, name="add_comment"),
    path('<str:user_username>/watchlist', views.watchlist, name="watchlist"),
    path('bid/<int:listing_id>', views.bid, name='bid'),
    path('add/<int:listing_id>', views.add_to_watch, name="add_to_watchlist"),
    path('close/<int:listing_id>', views.close_listing, name="close"),
    path('admin',views.index,name="admin"),
]
