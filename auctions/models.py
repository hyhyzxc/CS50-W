from unicodedata import decimal
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length = 64)
    description = models.CharField(max_length = 100)
    price = models.DecimalField(max_digits = 15, decimal_places = 2,)
    image = models.CharField(max_length = 500)
    category = models.CharField(max_length = 32, blank=True)
    lister = models.ForeignKey(User, on_delete = models.CASCADE)
    closed = models.BooleanField(default = False)
    watchlist = models.ManyToManyField(User, blank= True, related_name = "watchlists")

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE)
    bidder = models.ForeignKey(User, on_delete = models.CASCADE)
    bid_price = models.FloatField()

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete = models.CASCADE)
    item = models.ForeignKey(Listing, on_delete= models.CASCADE)
    comment = models.CharField(max_length = 100)



