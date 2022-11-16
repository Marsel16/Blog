from django.contrib import admin
from posts.models import Post, Hashtag

# Register your models here.
admin.site.register(Post)
admin.site.register(Hashtag)
