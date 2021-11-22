from django.shortcuts import render, redirect
from django.http import HttpResponse
from gardenApp.models import PublicUser
from django.contrib.auth import authenticate
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import PBKDF2PasswordHasher, check_password
import secrets
from utils.Geo import *

'''
Hashes a string
Using PBKDF2 with 32 byte salt
Returns string of password hash
'''
def hashPassword(plaintext):
    # hash password
    # random salt generation - 32 bytes should be secure enough
    uniqueSalt = secrets.token_urlsafe(32)
    passwordHash = PBKDF2PasswordHasher.encode(
        self=PBKDF2PasswordHasher,
        password=plaintext,
        salt=uniqueSalt
    )
    return passwordHash


'''
Checks the validity of a user in the local database.
routes based on validity of credentials
'''
def userLoginAuthentication(email, password):
    try:
        user = PublicUser.objects.get(email=email)
    except:
        return False
    if user is None:
        raise Exception("No such user")
    return check_password(password, user.pass_hash)


def home(request):
    return render(request, 'homepage.html')


def signup(request):
    return render(request, 'register.html')


def createUser(request):
    # get post request data
    username = request.POST.get("username")
    pw = request.POST.get("password")
    address = request.POST.get("address")
    email = request.POST.get("email")

    # hash password
    pw = hashPassword(pw)

    #TODO handle bad address
    location = addressToCoordinates(address)

    # create user
    #TODO catch user creation error
    # could be for already existing email
    # put it in a try except block
    # try:
    new = PublicUser.objects.create(
        email=email,
        username=username,
        pass_hash=pw,
        address=address,
        verified=False,
        latitude=location.latitude,
        longitude=location.longitude
    )
    new.save()

    # context = {
    #     #'id':new.id,
    #     #'email':new.email,
    #     'username':new.username,
    #     #'pass_hash':new.pass_hash,
    #     #'address':new.address,
    # }
    request.session['id'] = new.id
    response = redirect('/landing')
    return response
    # return render(request,'landing.html',context)

# TODO if session not active, need to redirect (to homepage probably)
# just wrote a quick fix
def landing(request):
    id = -1
    try:
        id = request.session['id']
    except:
        return redirect("/")
    user = PublicUser.objects.get(id=id)
    context = {
        'username': user.username,
    }
    return render(request, 'landing.html', context)


def signin(request):
    return render(request, 'sign-in.html', {})


def signout(request):
    try:
        del request.session['id']
        response = redirect('/')
        return response
    except:
        pass
    # TODO Handle hack3rs

# TODO handle nonexistent user/bad login info
# AKA username/password incorrect
def authenticate(request):
    email = request.POST.get("email")
    pw = request.POST.get("password")
    if (userLoginAuthentication(email, pw)):
        user = PublicUser.objects.get(email=email)
        request.session['id'] = user.id
        response = redirect('/landing')
        return response
    response = redirect('/signin')
    return response


# TEST METHODS
def test_home(request):
    return render(request, 'test/testhome.html', {})


def test_login(request):
    return render(request, 'test/testlogin.html', {})


def test_createUser(request):
    return render(request, 'test/testcreate.html', {})


def test_make(request):
    # get post request data
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

    # create user
    new = PublicUser.objects.create(email=email, username=username, pass_hash=pw)
    new.save()

    context = {
        'id': new.id,
        'email': new.email,
        'username': new.username,
        'pass_hash': new.pass_hash
    }
    return render(request, 'test/testdisplay.html', context)


def test_authenticate(request):
    username = request.POST.get("username")
    pw = request.POST.get("password")

    # DEBUG print parameters
    print('{} {}'.format(username, pw))

    # Only checks if user exists with given parameters
    # Need to implement TOKEN verification, as well as model based authentication
    try:
        # TODO should use email instead of username to login
        # TODO TEST pass authentication
        # NOTE need to set environment variable: DJANGO_SETTINGS_MODULE=garden.garden.settings
        user = PublicUser.objects.get(username=username)  # ,pass_hash=pw)
        valid = check_password(pw, user.pass_hash)

        if valid:
            return HttpResponse("<h1>{} IS LEGIT</h1><br><a href='/'>HOME</a>".format(user.username))
        else:
            # TODO bad login credential response
            return HttpResponse("<h1>NOT LEGIT</h1><br><a href='/'>HOME</a>")
    except:
        return HttpResponse("<h1>NOT LEGIT</h1><br><a href='/'>HOME</a>")
