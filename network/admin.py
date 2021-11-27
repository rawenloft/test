from django.contrib import admin
from .models import User, Post, Comment, Like

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "comment")

class LikeAdmin(admin.ModelAdmin):
    list_display = ("post", "author")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)