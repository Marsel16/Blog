from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    photo = models.ImageField()
    likes = models.IntegerField()
    hashtags = models.ManyToManyField('Hashtag', blank=True)


class Hashtag(models.Model):
    title = models.CharField(max_length=80)
    posts = models.ManyToManyField(Post, blank=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username}_{self.text}'
