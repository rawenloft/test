from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    follow = models.ManyToManyField("self", symmetrical=False, related_name="followers", blank=True, null=True)

class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    liked_by = models.ManyToManyField("User", related_name="liked_post")

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    comment = models.TextField(max_length=140, blank=True)

class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey("User", on_delete=models.CASCADE)