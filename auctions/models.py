from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

def __str__(self):
    return f"{self.id}: {self.username} \n {self.email} "

CATEGORIES = (
    ('Tools', 'Tools'),
    ('Books', 'Books'),
    ('Spells', 'Spells'),
    ('Potions', 'Potions'),
    ('Herbs', 'Herbs'),
    ('Others', 'Others'),
)

class Listing(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="item id")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=20, verbose_name="category", choices=CATEGORIES, blank=True)
    description = models.TextField(max_length=254)
    img_url = models.URLField(max_length=200, blank=True)
    start_bid = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

def __str__(self):
    return f"Author: {self.created_by} \n {self.title} \n {self.category}\n {self.img_url}\n {self.description}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="bid id")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    created_for = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_to_buy", default=True)
    start_bid =  models.IntegerField(default='1')
    highest_bid = models.IntegerField(default='1')
    highest_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner")
    started_at = models.DateTimeField(auto_now=False, auto_now_add=True)

def __str__(self):
    return f"Bidder: {self.created_by}, {self.start_bid}, {self.highest_bid}, {self.highest_bidder}, {self.started_at}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='comment id', unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    content = models.TextField(max_length=512)
    rel_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_aim")

def __str__(self):
    return f"{self.id}: {self.created_by}, {self.content}, {self.rel_listing}"


