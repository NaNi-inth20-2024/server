from django.db import models
from django.contrib.auth import get_user_model


MAX_AUCTION_TITLE_LENGTH = 50


class Auction(models.Model):
    title = models.CharField(max_length=MAX_AUCTION_TITLE_LENGTH)
    description = models.TextField()
    initial_bid = models.IntegerField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    active = models.BooleanField(default=True)


class Bid(models.Model):
    price = models.IntegerField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)


class AuctionPhoto(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='auction_photos/')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
