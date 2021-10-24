from django.db import models


# Create your models here.
#TODO set all lengths to a reasonable length
#TODO foreign keys
class PublicUser(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=256)
    pass_hash = models.CharField(max_length=256)
    #address = models.CharField(max_length=256)

    def __repr__(self):
        return str(self.__dict__)


class CorpUser(models.Model):
    email = models.EmailField()
    pass_hash = models.CharField(max_length=256)
    address = models.CharField(max_length=256)


class Produce(models.Model):
    produce_name = models.CharField(max_length=256)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    owner = models.ForeignKey(PublicUser, on_delete=models.CASCADE)  # foreign key


class Donation(models.Model):
    produce_id = "produce_id"  # foreign key
    donatee = "corp_user_id"  # foreign key
    date_created = models.DateField(auto_now_add=True)  # date time


class ProduceAlert(models.Model):
    produce_id = "produce_id"  # foreign key
    date_created = models.DateField(auto_now_add=True)  # date time


class ProduceRequest(models.Model):
    produce_name = models.CharField(max_length=256)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    corp_user = models.ForeignKey(CorpUser, on_delete=models.CASCADE)  # foreign key

class Article(models.Model):
    title = models.CharField(max_length=256)
    date = models.DateField() # set manually?
    author = models.CharField(max_length=64)
    content = models.TextField()