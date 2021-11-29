from django.shortcuts import render, redirect
from gardenApp.models import *
from utils.Geo import *
from utils.Authentication import *
from utils import Search
import datetime

def home(request):
    try:
        request.session['id']
        return redirect('landing')
    except:
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
    except Exception as e:
        print(str(e))
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
    except Exception as e:
        print(str(e))
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
    return render(request, 'createpost.html', {})

def createPost(request):
    produce_name = request.POST.get("name").lower()
    weight = request.POST.get("weight")
    t =request.POST.get("type")
    desc = request.POST.get('description')
    
    if t == "fruit":
        fruits = True
        veggies = False
    else:
        fruits = False
        veggies = True
    
    #owner = request.session['id']
    image = request.FILES.get('image')
    if image is None:
        params = {
            'produce_name':produce_name,
            'weight':float(weight),
            'fruits':fruits,
            'veggies':veggies,
            'owner':PublicUser.objects.get(id=request.session['id']),
            'description':desc
        }
    else:
        params = {

            'produce_name':produce_name,
            'weight':float(weight),
            'fruits':fruits,
            'veggies':veggies,
            'owner':PublicUser.objects.get(id=request.session['id']),
            'image':image,
            'description':desc
        }

    try: 
        new = Produce.objects.create(**params)
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
    prod = Produce.objects.filter(donated=False)
    context = {
        'username': user.username,
        'searchQuery': prod,
        'recieving' : True
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
    

    searchQuery = request.POST.get("search")
    recieving = True if request.POST.get("recieving") == 'on' else False
    
    prodType = request.POST.get('type')

    if prodType == 'fruit':
        fruits = True
        veggies = False
    elif prodType is None:
        fruits = False
        veggies = False
    else:
        fruits = False
        veggies = True
    
    distance = 0

    try:
        distance = int(request.POST.get("dist"))
    except:
        distance = 4294967295
    
    prodlist = Search.getLocalProduce(user, searchQuery, fruits, veggies, distance, recieving)
    print(prodlist)
    context = {
        'username' : user.username,
        'searchQuery': prodlist,
        'fruits'  : fruits,
        'veggies' : veggies,
        'recieving' : recieving
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
    donations = Search.getAllUserDonations(user)
    context = {
        'user' : user,
        'donations' : donations
    }
    return render(request, 'profile.html',context)

def changeProfileImage(request):
    image = request.FILES.get('image')
    user = PublicUser.objects.get(id=request.session['id'])
    user.image = image
    ##TODO delete previous image

    user.save()
    return redirect('/profile')

def manage(request):
    prod = Produce.objects.filter(owner=PublicUser.objects.get(id=request.session['id'])).exclude(donated=True).all()
    context = {
        'produce':prod
    }
    return render(request, 'posts.html', context)


def donation(request, id):
    prod = Produce.objects.get(id=id)
    context = {
        'prod': prod
    }
    return render(request, 'editpost.html', context)

def editDonation(request, id):
    print(request.POST)
    prod = Produce.objects.get(id=id)
    if request.POST.get('name') != '':
        prod.produce_name = request.POST.get('name')
    if request.POST.get('weight') != '':
        prod.weight = request.POST.get('weight')
    if request.POST.get('description') != '':
        prod.description = request.POST.get('description')
    prodType = request.POST.get('type')
    
    if prodType == 'fruit':
        prod.fruits = True
        prod.veggies = False
    elif prodType == 'veg':
        prod.fruits = False
        prod.veggies = True

    if request.FILES.get('image') is not None:
        prod.image = request.FILES.get('image')
    
    prod.date_created = datetime.datetime.now()
    prod.save()
    return redirect('/donation/{0}'.format(id))

def deleteDonation(request, id):
    Produce.objects.get(id=id).delete()
    return redirect('/landing')

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

    if user1 == user2: return redirect("/landing")
    
    try:
        Chat.objects.create(user1=user1, user2=user2)
    finally:
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
    
def createRequestPage(request):
    return render(request,'createrequest.html',{})

def createRequest(request):
    name = request.POST.get('name').lower()
    weight = float(request.POST.get('weight'))
    prodType = request.POST.get('type')

    if prodType == 'fruit':
        fruits = True
        veggies = False
    elif prodType is None:
        fruits = True
        veggies = True
    else:
        fruits = False
        veggies = True


    ProduceRequest.objects.create(
        produce_name = name,
        weight=weight,
        owner=PublicUser.objects.get(id=request.session['id']),
        fruits=fruits,
        veggies=veggies,
    )

    return redirect('/landing')

def manageRequestPage(request):
    user = PublicUser.objects.get(id=request.session['id'])
    prodList = ProduceRequest.objects.filter(owner=user)
    context = {
        'req':prodList
    }
    return render(request,'requests.html',context)

def editRequestPage(request, id):
    prod = ProduceRequest.objects.get(id=id)
    context = {
        'req':prod
    }
    return render(request,'editRequest.html', context)

def editRequest(request, id):
    prod = ProduceRequest.objects.get(id=id)

    if request.POST.get('name'):
        prod.produce_name = request.POST.get('name')
    if request.POST.get('weight'):
        prod.weight = float(request.POST.get('weight'))

    prodType = request.POST.get('type')
    if prodType == 'fruit':
        prod.veggies = False
        prod.fruits = True
    elif prodType == 'veg':
        prod.veggies = True
        prod.fruits = False
        
    prod.save()
    return redirect('/request/{0}'.format(id))

def deleteRequest(request, id):
    prod = ProduceRequest.objects.get(id=id).delete()
    return redirect('/managerequests')

def markAsDonated(request,id):
    produce = Produce.objects.get(id=id)
    produce.donated = True
    produce.save()

    Donation.objects.create(produce_id=produce)

    return redirect("/landing")


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
