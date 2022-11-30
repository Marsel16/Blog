from django.http import HttpResponse
from django.shortcuts import render, redirect
from users.forms import LoginForm
from django.contrib.auth import login, authenticate, logout
# Create your views here.
from users.utils import get_user_from_request


def login_view(request):
    if request.method == 'GET':
        data = {
            'form': LoginForm,
            'user': get_user_from_request(request)
        }
        return render(request, 'users/login.html', context=data)

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                surname=form.cleaned_data.get('surname'),
                password=form.cleaned_data.get('password'),
                password2=form.cleaned_data.get('password2')
            )
            if user:
                login(request, user)
                return redirect('/posts')
            else:
                form.add_error('плохой запрос')

        data = {
            'form': form
        }
        return render(request, 'users/login.html', context=data)

def logout_view(request):
    logout(request)
    return redirect('/posts')

