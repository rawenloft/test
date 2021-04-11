from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.get_random_page, name="random"),
    path("create", views.add_page, name="add"),
    path("edit/<str:title>", views.edit_page, name="edit"),
    path("search/", views.search, name="search"),
    path("<str:title>", views.get_page, name="page"),
    
]
