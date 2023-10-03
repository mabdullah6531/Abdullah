from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class bids(models.Model):
    price = models.IntegerField()
    highest_bidder = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    starting_bid = models.IntegerField(default=0)
    def default_starting(self):
        return self.price
    def save(self, *args, **kwargs):
        if not self.starting_bid:
            self.starting_bid = self.default_starting()
        super(bids, self).save(*args, **kwargs)
    

class YourModel(models.Model):
    title = models.CharField(max_length=64)
    bid = models.ForeignKey(bids, on_delete=models.CASCADE)
    image = models.URLField(default=None)
    category = models.CharField(max_length=64, default=None)
    description = models.TextField(default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    closed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class comments(models.Model):
    yourmodel = models.ForeignKey(YourModel, on_delete=models.CASCADE, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    message = models.CharField(max_length=255, default=None)


class watchlist(models.Model):
    yourmodel = models.ForeignKey(YourModel, on_delete=models.CASCADE, default="")    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")

class auctionswon(models.Model):
    title = models.CharField(max_length=64)
    bid = models.ForeignKey(bids, on_delete=models.CASCADE)
    image = models.URLField()
    category = models.CharField(max_length=64, default=None)
    description = models.TextField(default=None)