from django.contrib import admin
from .models import User, Listing, Bid, Comment, Watchlist
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'title', 'category', 'description', 'img_url', 'active', 'created_at')

class BidAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'start_bid', 'bid', 'listing_id', 'started_at')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'content', 'rel_listing')


admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist)