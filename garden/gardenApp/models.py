from django.db import models


# Create your models here.
class PublicUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=64)
    pass_hash = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    verified = models.BooleanField(default=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to="profile_images/", null=True)

    def __repr__(self):
        return str(self.__dict__)


class Produce(models.Model):
    produce_name = models.CharField(max_length=64)
    weight = models.FloatField()
    fruits = models.BooleanField()
    veggies = models.BooleanField()
    owner = models.ForeignKey(PublicUser, on_delete=models.CASCADE)  # foreign key
    date_created = models.DateField(auto_now_add=True)  # date time
    image = models.ImageField(upload_to="produce_images/", null=True)



class Donation(models.Model):
    produce_id = models.ForeignKey(Produce, on_delete=models.CASCADE)  # foreign key
    reciever = models.ForeignKey(PublicUser, on_delete=models.CASCADE)  # foreign key
    date_created = models.DateField(auto_now_add=True)  # date time


class ProduceRequest(models.Model):
    produce_name = models.CharField(max_length=64)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(PublicUser, on_delete=models.CASCADE)  # foreign key

# #message system
# #TODO get chat working
# class Chat(models.Model):
#     user1 = models.ForeignKey(PublicUser, related_name='user1', on_delete=models.CASCADE)
#     user2 = models.ForeignKey(PublicUser, related_name='user2', on_delete=models.CASCADE)
#     messages = models.ManyToOneRel()


# class Message(models.Model):
#     userID = models.ForeignKey(PublicUser, related_name='sender', on_delete=models.CASCADE)
#     chatID = models.ForeignKey(Chat)
#     msg = models.TextField()
#     dateTime = models.DateTimeField(auto_created=True)


#     def __repr__(self):
#         return str(self.__dict__)

# class Article(models.Model):
#     title = models.CharField(max_length=64)
#     date = models.DateField()  # set manually?
#     author = models.CharField(max_length=64)
#     content = models.TextField()

