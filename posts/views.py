from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post, Hashtag, Comment
from .forms import PostCreateForm, CommentCreateForm
from users.utils import get_user_from_request

# Create your views here.
PAGINATION_LIMIT = 3

def posts_view(request):
    if request.method == 'GET':
        search_text = request.GET.get('search')
        hashtag_id = request.GET.get('hashtag_id')
        page = int(request.GET.get('page', 1))
        if hashtag_id:
            posts = Post.objects.filter(hashtag=Hashtag.objects.get(id=hashtag_id))
        else:
            posts = Post.objects.all()
        if search_text:
            posts = posts.filter(title__icontains=search_text)
        max_page = round(posts.__len__() / PAGINATION_LIMIT)
        page = int(page)
        posts = posts[PAGINATION_LIMIT * (page - 1): PAGINATION_LIMIT * page]
        data = {
            'posts': posts,
            'user': get_user_from_request(request),
            'hashtag_id': hashtag_id,
            'current_page': page,
            "search_text": search_text,
            'max_page': list(range(1, max_page + 1))
        }
        return render(request, 'posts/posts.html', context=data)


def hashtags_view(request):
    if request.method == 'GET':
        hashtags = Hashtag.objects.all()
        data = {
            'hashtags': hashtags,
            'user': get_user_from_request(request)
        }
        return render(request, 'hashtags/hashtags.html', context=data)


def detail_view(request, **kwargs):
    if request.method == 'GET':
        post = Post.objects.get(id=kwargs['id'])

        data = {
            'post': post,
            'comments': Comment.objects.filter(post=post),
            'form': CommentCreateForm,
            'user': get_user_from_request(request)
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
                'form': form,
                'user': get_user_from_request(request)
            }
            return render(request, 'posts/detail.html', context=data)


def posts_create_view(request):
    if request.method == 'GET':
        data = {
            'form': PostCreateForm,
            'user': get_user_from_request(request)
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
                'form': form,
                'user': get_user_from_request(request)
            }
            return render(request, 'posts/create.html', context=data)
