from gardenApp.models import PublicUser, Produce, ProduceRequest, Chat, Message
from utils.Geo import coordinateDistance
from django.db.models import Q


# Helper function
def getLocalUsers(currUser, miles):
    allUsers = PublicUser.objects.all().exclude(email=currUser.email)
    nearbyUsers = []

    coord1 = (currUser.latitude, currUser.longitude)

    for user in allUsers:
        coord2 = (user.latitude, currUser.longitude)

        distanceMiles = coordinateDistance(coord1, coord2)

        if distanceMiles <= miles:
            nearbyUsers.append(user)

    return nearbyUsers


"""
currUser = models.PublicUser
searchQuery = string
fruits, veggies = bool
miles = number
"""
def getLocalProduce(currUser, searchQuery, fruits, veggies, miles, recieving):
    nearbyUsers = getLocalUsers(currUser, miles)
    nearbyProduce = []

    searchQuery = searchQuery.lower()
    
    # decide with database to search through if user is giving or recieving
    if recieving:
        databaseToSearch = Produce
        param = {'donated':False}
    else:
        databaseToSearch = ProduceRequest
        param = {}

    for user in nearbyUsers:
        if ((not fruits and not veggies) or (fruits and veggies)):
            param.update({'owner':user})
        else:
            param.update({'owner':user, "fruits":fruits, "veggies":veggies})
        
        produce_query_set = databaseToSearch.objects.filter(**param).all()
        print(produce_query_set)
        for produce in produce_query_set:
            if produce is not None and (searchQuery in produce.produce_name.lower() or produce.produce_name.lower() in searchQuery):
                nearbyProduce.append(produce)

    return nearbyProduce

def getAllChatsForUser(currUser):
    chatList = list(Chat.objects.filter(Q(user1=currUser) | Q(user2=currUser)))
    return chatList

def getAllMessagesInChat(chat):
    msgList = list(Message.objects.filter(chatID=chat))
    return sorted(msgList, key=lambda x: x.dateTime)


def getAllUserDonations(currUser):
    allDonations = Produce.objects.filter(owner=currUser, donated=True).all()
    return allDonations


