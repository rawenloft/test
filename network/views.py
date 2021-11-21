from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import User, Post, Comment


def index(request):
    user = request.user
    return render(request, "network/index.html")

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):
    if request.method == "POST":
        author = request.user
        post = request.POST["post"]

        try:
            new_post = Post.objects.create(author=author, post=post, created_at=True)
            new_post.save()
            message = "Posted successfully"
            return render(request, "network/index.html", {
                "message": message,
                "show_user": author,
            })
        except Error:
            message = "Your post is empty. Please write something."
            return render(request, "network/new_post.html", {
                "message": message,
            })
    return render(request, "network/new_post.html")

def get_all_post(request):
    user = request.user
    posts = Post.objects.all().order_by('-created_at')
    posts_count = Post.objects.filter(author=user).count
    return render(request, "network/index.html",{
        "posts": posts,
        "posts_count": posts_count,
        "show_user": user,
    })

def show_profile(request, user):
    find_user = User.objects.filter(username=user).first()
    posts = Post.objects.filter(author=find_user).order_by('-created_at')
    posts_count = Post.objects.filter(author=find_user).count
    signal = True
# posts = Post.objects.all().order_by('-created_at')
# posts_count = Post.objects.filter(author=user).count
    return render(request, "network/index.html", {
        "posts": posts,
        "posts_count": posts_count,
        "show_user": find_user,
        "signal": signal,
    })