from django.contrib import admin
from .models import User, Post, Comment

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("commenter", "comment", "rel_post")
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

