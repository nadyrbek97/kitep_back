from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .forms import UserLoginForm, UserRegisterForm


def user_register(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password2')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Account for {} was created successfully'.format(username))

            return redirect('index-page-view')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register_form.html', {'form': form})


def user_login(request):

    if request.method == "POST":
        form = UserLoginForm(request.POST)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You've logged in successfully")
        return redirect('index-page-view')
    else:
        form = UserLoginForm()

    return render(request, 'users/login_form.html', {'form': form})
