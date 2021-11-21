from gardenApp.models import PublicUser, Produce
from utils.Geo import coordinateDistance

#TODO documentation

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

def getLocalProduce(currUser, searchQuery, fruits, veggies, miles):
    nearbyUsers = getLocalUsers(currUser, miles)
    nearbyProduce = []

    for user in nearbyUsers:
        produce_query_set = Produce.objects.filter(owner=user, fruits=fruits, veggies=veggies).all()

        for produce in produce_query_set:
            if produce is not None and searchQuery in produce.produce_name:
                nearbyProduce.append(produce)

    return nearbyProduce
