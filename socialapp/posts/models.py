from django.db import models
from django.conf import settings
from django.urls import reverse

import misaka
from groups.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now = True)
    message = models.TextField()
    message_html = models.TextField(editable = False)
    group = models.ForeignKey(Group, on_delete = models.CASCADE, related_name='posts', null=True, blank=True)
    liked_users = models.ManyToManyField(User, through='PostLike')

     
    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.message
    
    def get_absolute_url(self):
        return reverse("posts:single", kwargs={"username": self.user.username,
                                              "pk": self.pk})
       
    class Meta:
        ordering = ["-created_at"]
        unique_together = ("user", "message")


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("post", "user")
   
