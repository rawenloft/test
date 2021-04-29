from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=20, verbose_name="category", choices=CATEGORIES, blank=True)
    description = models.TextField(max_length=254)
    img_url = models.URLField(max_length=200, blank=True)
    start_bid = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)

def __str__(self):
    return f"Author: {self.created_by} {self.title} {self.category} {self.img_url} {self.description} {self.created_at}"

class Bid(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_to_buy", default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    start_bid =  models.IntegerField()
    bid = models.IntegerField(null=True)
    started_at = models.DateTimeField(auto_now=False, auto_now_add=True,)

def __str__(self):
    return f"Bidder: {self.created_by}, {self.bid}, for: {self.listing_id}, {self.started_at}"


class Comment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    content = models.TextField(max_length=512)
    rel_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_aim")

def __str__(self):
    return f"{self.id}: {self.created_by}, {self.content}, {self.rel_listing}"


