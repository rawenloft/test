from django.contrib import admin
from .models import User, Follow, Post, Comment, Like

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "following_user_id")

class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "comment")

class LikeAdmin(admin.ModelAdmin):
    list_display = ("post", "author")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)