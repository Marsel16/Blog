from django.http import HttpResponse
from django.shortcuts import render
from .models import Post, Hashtag, Comment

# Create your views here.
def posts_view(request):
    if request.method == 'GET':
        data = {
            'posts': Post.objects.all()
        }
        return render(request, 'posts/posts.html', context=data)


def hashtags_view(request):
    if request.method == 'GET':
        hashtags = Hashtag.objects.all()
        data = {
            'hashtags': hashtags
        }
        return render(request, 'hashtags/hashtags.html', context=data)

def detail_view(request, **kwargs):
    if request.method == 'GET':
        post = Post.objects.get(id=kwargs['id'])

        data = {
            'post': post,
            'comments': Comment.objects.filter(post=post)
        }

        return render(request, 'posts/detail.html', context=data)
