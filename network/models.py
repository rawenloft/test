from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint

class User(AbstractUser):
    follow = models.ManyToManyField("self", symmetrical=False, related_name="followers", blank=True, null=True)

class Post(models.Model):
    author = models.ForeignKey(User, related_name="author", on_delete=models.CASCADE)
    post = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    like = models.IntegerField(default=0)
    
class Comment(models.Model):
    rel_post = models.ForeignKey(Post, related_name="comment_post", on_delete=models.CASCADE)
    comment = models.TextField(blank=True, max_length=100)
    commenter = models.ForeignKey(User, related_name="commenter", on_delete=models.CASCADE)
