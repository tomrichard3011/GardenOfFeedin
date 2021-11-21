from geopy import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="GardenOfFeedin")
'''
returns geocode object, retrieve with loation.latitude and location.longitude
'''
def addressToCoordinates(address):
    location = geolocator.geocode(address)
    if location is None: # invalid address
        raise Exception("Invalid or Nonexistent address given")

    return location

'''
Finds the distance in miles from two coordinates
(lat, long)
'''
def coordinateDistance(coord1, coord2):
    return geodesic(coord1, coord2).mi

