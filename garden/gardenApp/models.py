from django.db import models
import os


# Create your models here.
class PublicUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=64)
    pass_hash = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    verified = models.BooleanField(default=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to="profile_images", default="profile_images/default_profile.png")
    # total_donated = models.FloatField(default=0)

    def __repr__(self):
        return str(self.__dict__)


class Produce(models.Model):
    produce_name = models.CharField(max_length=64)
    weight = models.FloatField()
    fruits = models.BooleanField()
    veggies = models.BooleanField()
    owner = models.ForeignKey(PublicUser, on_delete=models.CASCADE)  # foreign key
    date_created = models.DateField(auto_now_add=True)  # date time
    image = models.ImageField(upload_to="produce_images", default="produce_images/default_produce.jpg")
    description = models.TextField(null=True)
    # donated = models.BooleanField(default=False)


    def __repr__(self):
        return str(self.__dict__)


class Donation(models.Model):
    produce_id = models.ForeignKey(Produce, on_delete=models.CASCADE)  # foreign key
    date_created = models.DateField(auto_now_add=True)  # date time

    def __repr__(self):
        return str(self.__dict__)


class ProduceRequest(models.Model):
    produce_name = models.CharField(max_length=64)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    owner = models.ForeignKey(PublicUser, on_delete=models.CASCADE)  # foreign key
    fruits = models.BooleanField()
    veggies = models.BooleanField()

# #message system
#TODO get chat working
class Chat(models.Model):
    user1 = models.ForeignKey(PublicUser, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(PublicUser, related_name='user2', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user1', 'user2']
    
    def __repr__(self):
        return str(self.__dict__)


class Message(models.Model):
    userID = models.ForeignKey(PublicUser, on_delete=models.CASCADE)
    chatID = models.ForeignKey(Chat, on_delete=models.CASCADE)
    msg = models.TextField()
    dateTime = models.DateTimeField(auto_now_add=True)


    def __repr__(self):
        return str(self.__dict__)

