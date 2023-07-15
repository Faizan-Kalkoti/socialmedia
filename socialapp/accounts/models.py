from django.db import models
from django.contrib import auth
from django.contrib.auth.models import PermissionsMixin, User as User_pic

class User(User_pic, PermissionsMixin):
    
    def __str__(self):
        return "@{}".format(self.username)
    
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User_pic, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    user_description = models.TextField(blank = True)

    def __str__(self) -> str:
        return self.user.username

# Create your models here.
 