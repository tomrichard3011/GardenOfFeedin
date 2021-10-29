from django.shortcuts import render, redirect
from django.http import HttpResponse
from gardenApp.models import PublicUser
from django.contrib.auth import authenticate
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import PBKDF2PasswordHasher, check_password
import secrets

def test_home(request):
    return render(request, 'test/testhome.html', {})

def test_login(request):
    return render(request, 'test/testlogin.html',{})

def test_createUser(request):
    return render(request, 'test/testcreate.html', {})

def test_make(request):
    #get post request data
    username = request.POST.get("username")
    pw = request.POST.get("password")
    email = request.POST.get("email")

    # hash password
    # random salt generation - 32 bytes should be secure enough
    uniqueSalt = secrets.token_urlsafe(32)
    pw = PBKDF2PasswordHasher.encode(
        self=PBKDF2PasswordHasher,
        password=pw,
        salt=uniqueSalt
    )



    #create user
    new = PublicUser.objects.create(email=email,username=username,pass_hash=pw)
    new.save()

    context = {
        'id':new.id,
        'email':new.email,
        'username':new.username,
        'pass_hash':new.pass_hash
    }
    return render(request,'test/testdisplay.html',context)


def test_authenticate(request):
    username = request.POST.get("username")
    pw = request.POST.get("password")

    #DEBUG print parameters 
    print('{} {}'.format(username, pw))

    #Only checks if user exists with given parameters
    #Need to implement TOKEN verification, as well as model based authentication
    try:
        #TODO should use email instead of username to login
        #TODO TEST pass authentication
        #NOTE need to set environment variable: DJANGO_SETTINGS_MODULE=garden.garden.settings
        user = PublicUser.objects.get(username=username) #,pass_hash=pw)
        valid = check_password(pw, user.pass_hash)

        if valid:
            return HttpResponse("<h1>{} IS LEGIT</h1><br><a href='/'>HOME</a>".format(user.username))
        else:
            # TODO bad login credential response
            return HttpResponse("<h1>NOT LEGIT</h1><br><a href='/'>HOME</a>")
    except: 
        return HttpResponse("<h1>NOT LEGIT</h1><br><a href='/'>HOME</a>")

