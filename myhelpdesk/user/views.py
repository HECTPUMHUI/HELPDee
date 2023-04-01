from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token

from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request, 'user/register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('index')
            elif user is not None and user.is_user:
                login(request, user)
                return redirect('index')
            else:
                msg = 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'user/login.html', {'form': form, 'msg': msg})


def logout_user(request):
    if request.user.is_authenticated:
        Token.objects.filter(user=request.user).delete()
        logout(request)
    return redirect('index')
