from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Follow, Post, Comment, Like


def index(request):
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

def profile(request, user):
    me = request.user
    if me.is_authenticated:
        user = User.objects.filter(username=user)
        all_follows = Follow.objects.filter(user_id=user.first()).count()
        all_following = Follow.objects.filter(following_user_id=user.first()).count()
        show_user = user[0]
        if show_user != me:
            posts = Post.objects.filter(author=show_user)
        else:
            posts = Post.objects.filter(author=me)

        check_follow = Follow.objects.filter(user_id=me, following_user_id=user.first())
        flag = False
        if check_follow:
            flag = True
        else:
            flag = False
        return render(request, "network/profile.html", {
            "profile_user": show_user,
            "flag": flag,
            "follow_count": all_follows,
            "following_count": all_following,
            "posts": posts,
        })
    return HttpResponseRedirect(reverse("index"))

def follow(request, user):
    me = request.user
    follow = User.objects.get(username=user)
    check_follow = Follow.objects.filter(user_id=me, following_user_id=follow)
    if check_follow:
        check_follow.delete()
    else:
        follow_user = Follow.objects.create(user_id=me, following_user_id=follow)
        follow_user.save()
    print(me, follow)
    return HttpResponseRedirect(reverse('profile', args=[follow]))

def all_posts(request):
    me = request.user
    posts = Post.objects.all().order_by("-created_at")
    posts_count = Post.objects.filter(author=me).count
    return render(request, "network/posts.html", {
        "posts": posts,
        "posts_count": posts_count,
    })

def new_post(request):
    if request.method == "POST":
        try:
            author = request.user
            post = request.POST["post"]
            print(post, author)
            new_post = Post.objects.create(author=author, post=post, created_at=True)
            new_post.save()
            message = "Posted successfully"
            print(message)
            return render(request, "network/profile.html", {
                "message": message,
                "user": author,
                "profile_user": author,
            })
        except:
            message = "Your post is empty. Please write something."
            print(message)
            return render(request, "network/profile.html", {
                "message": message,
                "user": author,
                "profile_user": author,
            })