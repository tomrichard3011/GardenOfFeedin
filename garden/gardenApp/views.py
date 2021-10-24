from django.shortcuts import render, redirect
from django.http import HttpResponse
from gardenApp.models import PublicUser
from django.contrib.auth import authenticate
from django.contrib.auth.backends import BaseBackend
#import bcrypt #later for password hash

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

    #create user
    new = PublicUser.objects.create(email=email,username=username,pass_hash=pw)
    new.save()

    context = {
        'id':new.id,
        'email':new.email,
        'username':new.username,
        'pass_hash':new.pass_hash
    }
    return render(request,'test/display.html',context)


def test_authenticate(request):
    username = request.POST.get("username")
    pw = request.POST.get("password")

    #DEBUG print parameters 
    print('{} {}'.format(username,pw))

    #Only checks if user exists with given parameters
    #Need to implement TOKEN verification, as well as model based authentication
    try:
        user = PublicUser.objects.get(username=username,pass_hash=pw)
        if user is not None:
            return HttpResponse("<h1>{} IS LEGIT</h1><br><a href='/'>HOME</a>".format(user.username))
    except: 
        return HttpResponse("<h1>NOT LEGIT</h1><br><a href='/'>HOME</a>")

