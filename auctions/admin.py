from django.contrib import admin
from .models import User, Listing, Bid, Comment
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'title', 'category', 'description', 'img_url', 'active')

class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'start_bid', 'highest_bid', 'highest_bidder', 'started_at')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'content', 'rel_listing')

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
