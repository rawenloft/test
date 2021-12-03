from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    pass

class Follow(models.Model):
    user_id = models.ForeignKey("User",related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey("User",related_name="followers", on_delete=models.CASCADE)

    class Meta:
        models.UniqueConstraint(fields=['user_id', 'following_user_id'], name='%(app_label)s_unique_follow')

class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    liked_by = models.ManyToManyField("User", related_name="liked_post", null=True, blank=True)

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    comment = models.TextField(max_length=140, blank=True)

class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey("User", on_delete=models.CASCADE)