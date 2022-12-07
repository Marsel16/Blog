from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post, Hashtag, Comment
from .forms import PostCreateForm, CommentCreateForm
from users.utils import get_user_from_request
from django.views.generic import ListView, CreateView, DetailView

# Create your views here.
PAGINATION_LIMIT = 3


class PostView(ListView):
    template_name = 'posts/posts.html'
    queryset = Post.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        search_text = self.request.GET.get('search')
        hashtag_id = self.request.GET.get('hashtag_id')
        page = int(self.request.GET.get('page', 1))
        if hashtag_id:
            posts = Post.objects.filter(hashtag=Hashtag.objects.get(id=hashtag_id))
        else:
            posts = Post.objects.all()
        if search_text:
            posts = posts.filter(title__icontains=search_text)
        max_page = round(posts.__len__() / PAGINATION_LIMIT)
        page = int(page)
        posts = posts[PAGINATION_LIMIT * (page - 1): PAGINATION_LIMIT * page]
        return {
            'posts': posts,
            'user': get_user_from_request(self.request),
            'hashtag_id': hashtag_id,
            'current_page': page,
            "search_text": search_text,
            'max_page': list(range(1, max_page + 1))
        }


class HashtagsView(ListView):
    model = Hashtag
    queryset = Hashtag.objects.all()
    template_name = 'hashtags/hashtags.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'object_list': self.get_queryset(),
            'user': get_user_from_request(self.request)
        }


class PostDetailView(DetailView, CreateView):
    template_name = 'posts/detail.html'
    queryset = Post.objects.all()
    form_class = PostCreateForm
    pk_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        post = self.get_object()
        return {
            'post': post,
            'comments': Comment.objects.filter(post=post),
            'form': CommentCreateForm,
            'user': get_user_from_request(self.request)
        }

    def post(self, request, *args, **kwargs):
        form = CommentCreateForm(data=request.POST)

        if form.is_valid():
            Comment.objects.create(
                author=request.user,
                text=form.cleaned_data.get('text'),
                post_id=self.get_object().id
            )
            return redirect(f'/posts/{self.get_object().id}/')
        return render(request, self.template_name, context=self.get_context_data(form=form))

class PostCreateView(CreateView):
    form_class = PostCreateForm
    template_name = 'posts/create.html'
    def get_context_data(self, **kwargs):
        return {
            'form': PostCreateForm,
            'user': get_user_from_request(self.request)
        }
    def post(self, request, *args, **kwargs):
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
            return render(request, self.template_name,self.get_context_data(form=form))

def main_page_view(request):
    return render(request, 'main_page/main_page.html')
