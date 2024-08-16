# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login,  logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import requests

def updatePasswordRequest(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.info(request, 'Ubah Password sukses, Silahkan login lagi!!')
            logout(request)
            return redirect('login')
        else:
            messages.info(request, 'Berikan password yang benar sesuai format..!!')
            return redirect('update_password')
    else:
        form = PasswordChangeForm(user=request.user)
        
    context = {'form' : form}
    return render(request, 'accounts/update_password.html', context)

@csrf_exempt
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.info(request, 'Invalid credentials')
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})

@csrf_exempt
def register_user(request):
    msg = None
    success = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

def getngrok(request):
    try:
        r = requests.get('http://localhost:4040/api/tunnels')
        result = r.json()['tunnels'][0]['public_url']
    except:
        result = "NGROK Failed"    
    return HttpResponse(result)