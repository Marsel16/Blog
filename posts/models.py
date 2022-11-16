from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    photo = models.ImageField()
    likes = models.IntegerField()
    hashtags = models.ManyToManyField('Hashtag', blank=True)


class Hashtag(models.Model):
    title = models.CharField(max_length=80)
    posts = models.ManyToManyField(Post, blank=True)
