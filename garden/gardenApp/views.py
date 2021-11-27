from django.shortcuts import render, redirect
from gardenApp.models import *
from utils.Geo import *
from utils.Authentication import *
from utils import Search

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
    try:
        location = addressToCoordinates(address)
    except:
        return redirect("/signup")

    # create user
    #TODO catch user creation error
    # could be for already existing email
    # put it in a try except block

    try:
        new = PublicUser.objects.create(
        email=email,
        username=username,
        pass_hash=pw,
        address=address,
        verified=False,
        latitude=location.latitude,
        longitude=location.longitude
        )
    except:
        return redirect('/signup')

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
# should add that to every possible page?
# just wrote a quick fix

def createPostPage(request):
    return render(request, 'test/testpost.html', {})

def createPost(request):
    produce_name = request.POST.get("name")
    weight = request.POST.get("weight")
    t =request.POST.get("type")
    #fruits = ""
    #veggies = ""
    if t == "fruit":
        fruits = True
        veggies = False
    else:
        fruits = False
        veggies = True
    
    #owner = request.session['id']
    image = request.FILES.get('image')

    ##################################
    # # FOR DEBUGGING
    # print(produce_name)
    # print(weight)
    # print(fruits)
    # print(veggies)
    # print(owner)
    # print(image)
    ##################################

    try: 
        new = Produce.objects.create(
            produce_name=produce_name,
            weight=float(weight),
            fruits=fruits,
            veggies=veggies,
            owner=PublicUser.objects.get(id=request.session['id']),
            image=image
        )
    except Exception as e:
        print(e)
        return redirect('/createpost')
    
    return redirect('/landing')

def landing(request):
    id = -1
    try:
        id = request.session['id']
    except:
        return redirect("/")
    user = PublicUser.objects.get(id=id)
    prod = Produce.objects.all()
    context = {
        'username': user.username,
        'searchQuery': prod
    }
    print('{} is logged in'.format(user.username))
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

def search(request):
    id = request.session['id']
    user = PublicUser.objects.get(id=id)
    
    print(request.POST)

    searchQuery = request.POST.get("search")
    recieving = True if request.POST.get("recieving") == 'on' else False
    
    fruits = True if request.POST.get("fruit") == 'on' else False
    veggies = True if request.POST.get("vegetable") == 'on' else False
    distance = 0
    try:
        distance = int(request.POST.get("dist"))
    except:
        distance = 1000
    
    prodlist = Search.getLocalProduce(user, searchQuery, fruits, veggies, distance, recieving)
    print(prodlist)
    context = {
        'name' : user.username,
        'searchQuery': prodlist
    }

    return render(request, 'landing.html', context)

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

def profile(request):
    user = PublicUser.objects.get(id=request.session['id'])
    context = {
        'user' : user
    }
    return render(request, 'test/testprofile.html',context)

def changeProfileImage(request):
    image = request.FILES.get('image')
    user = PublicUser.objects.get(id=request.session['id'])
    user.image = image
    ##TODO delete previous image

    user.save()
    return redirect('/profile')

def manage(request):
    print("HERE")
    prod = Produce.objects.filter(owner=PublicUser.objects.get(id=request.session['id']))
    prod = list(prod)
    print(prod)
    context = {
        'produce':prod
    }
    return render(request, 'test/testmanage.html', context)


def donation(request, id):
    prod = Produce.objects.get(id=id)
    print(prod)
    context = {
        'prod': prod
    }
    return render(request, 'test/testdonation.html', context)

def editDonation(request, id):
    print(request.POST)
    prod = Produce.objects.get(id=id)
    if request.POST.get('name') != '':
        prod.produce_name = request.POST.get('name')
    if request.POST.get('weight') != '':
        prod.weight = request.POST.get('weight')
    prod.save()
    return redirect('/donation/{0}'.format(id))

def messages(request):
    user = PublicUser.objects.get(id=request.session['id'])
    chats = Search.getAllChatsForUser(user)
    context = {}
    allUserMsgs = []
    for chat in chats:
        allmsgs = Search.getAllMessagesInChat(chat)
        allUserMsgs.extend(allmsgs)
        
    context['chats'] = chats
    context['allmsgs'] = allUserMsgs
    print(context)
    return render(request,'test/testmessages.html',context)

def createChat(request):
    users = [
        PublicUser.objects.get(id=request.session['id']),
        PublicUser.objects.get(id=request.POST.get('user'))
    ]

    users.sort(key=lambda x: x.username)
    user1 = users[0]
    user2 = users[1]

    print(user1.username)
    print(user2.username)
    Chat.objects.create(user1=user1, user2=user2)
    return redirect('/messages')
    
def createMessage(request):
    chatID = Chat.objects.get(id=request.POST.get('chatID'))
    user = PublicUser.objects.get(id=request.session['id'])
    msg = request.POST.get('msg')

    Message.objects.create(
        chatID=chatID,
        userID=user,
        msg=msg
    )

    return redirect('/messages')
    

# # TEST METHODS
# def test_home(request):
#     return render(request, 'test/testhome.html', {})


# def test_login(request):
#     return render(request, 'test/testlogin.html', {})


# def test_createUser(request):
#     return render(request, 'test/testcreate.html', {})


# def test_make(request):
#     # get post request data
#     username = request.POST.get("username")
#     pw = request.POST.get("password")
#     email = request.POST.get("email")

    # hash password
    # pw = hashPassword(pw)

    # create user
    # new = PublicUser.objects.create(email=email, username=username, pass_hash=pw)

#     context = {
#         'id': new.id,
#         'email': new.email,
#         'username': new.username,
#         'pass_hash': new.pass_hash
#     }
#     return render(request, 'test/testdisplay.html', context)


# def test_authenticate(request):
#     username = request.POST.get("username")
#     pw = request.POST.get("password")

#     # DEBUG print parameters
#     print('{} {}'.format(username, pw))

#     # Only checks if user exists with given parameters
#     # Need to implement TOKEN verification, as well as model based authentication
#     try:
#         # TODO should use email instead of username to login
#         # TODO TEST pass authentication
#         # NOTE need to set environment variable: DJANGO_SETTINGS_MODULE=garden.garden.settings
#         user = PublicUser.objects.get(username=username)  # ,pass_hash=pw)
#         valid = check_password(pw, user.pass_hash)

#         if valid:
#             return HttpResponse("<h1>{} IS LEGIT</h1><br><a href='/'>HOME</a>".format(user.username))
#         else:
#             # TODO bad login credential response
#             return HttpResponse("<h1>NOT LEGIT</h1><br><a href='/'>HOME</a>")
#     except:
#         return HttpResponse("<h1>NOT LEGIT</h1><br><a href='/'>HOME</a>")
