from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('listing/<int:listing_id>', views.listing, name="listing"),
    path('create', views.create, name="create"),
    path('categories', views.categories, name="categories"),
    path('categories/<str:category>', views.category, name="category"),
    path('<int:listing_id>', views.add_comment, name="add_comment"),
    path('bid/<int:listing_id>', views.bid, name='bid')
]
