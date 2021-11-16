from django.db import models


# Create your models here.
class PublicUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=64)
    pass_hash = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    verified = models.BooleanField()
    latitude = models.DecimalField(max_digits=6, decimal_places=4)
    longitude = models.DecimalField(max_digits=6, decimal_places=4)
    #profile picture

    def __repr__(self):
        return str(self.__dict__)


class Produce(models.Model):
    produce_name = models.CharField(max_length=64)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    owner = models.ForeignKey(PublicUser, on_delete=models.CASCADE)  # foreign key


class Donation(models.Model):
    produce_id = models.ForeignKey(Produce, on_delete=models.CASCADE)  # foreign key
    reciever = models.ForeignKey(PublicUser, on_delete=models.CASCADE)  # foreign key
    date_created = models.DateField(auto_now_add=True)  # date time


class ProduceAlert(models.Model):
    produce_id = models.ForeignKey(Produce, on_delete=models.CASCADE)  # foreign key
    date_created = models.DateField(auto_now_add=True)  # date time


class ProduceRequest(models.Model):
    produce_name = models.CharField(max_length=64)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    corp_user = models.ForeignKey(PublicUser, on_delete=models.CASCADE)  # foreign key


class Article(models.Model):
    title = models.CharField(max_length=64)
    date = models.DateField()  # set manually?
    author = models.CharField(max_length=64)
    content = models.TextField()
