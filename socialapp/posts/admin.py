from django.contrib import admin
from posts.models import Post, PostLike
# Register your models here.


admin.site.register(Post)
admin.site.register(PostLike)


