from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post, Hashtag, Comment
from .forms import PostCreateForm, CommentCreateForm


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
            'comments': Comment.objects.filter(post=post),
            'form': CommentCreateForm
        }

        return render(request, 'posts/detail.html', context=data)

    if request.method == 'POST':
        form = CommentCreateForm(data=request.POST)

        if form.is_valid():
            Comment.objects.create(
                author_id=1,
                text=form.cleaned_data.get('text'),
                post_id=kwargs['id']
            )
            return redirect(f'/posts/{kwargs["id"]}/')
        else:
            post = Post.objects.get(id=kwargs['id'])
            comments = Comment.objects.filter(post=post)

            data = {
                'post': post,
                'comments': comments,
                'form': form
            }
            return render(request, 'posts/detail.html', context=data)

def posts_create_view(request):
    if request.method == 'GET':
        data = {
           'form': PostCreateForm
        }
        return render(request, 'posts/create.html', context=data)
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST)

        if form.is_valid():
            Post.objects.create(
                title=form.cleaned_data.get('title'),
                likes=form.cleaned_data.get('likes'),
            )
            return redirect('/posts/')
        else:
            data = {
                'form': form
            }
            return render(request, 'posts/create.html', context=data)
