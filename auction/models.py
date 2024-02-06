from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

MAX_AUCTION_TITLE_LENGTH = 50


class Auction(models.Model):
    title = models.CharField(max_length=MAX_AUCTION_TITLE_LENGTH)
    description = models.TextField()
    initial_price = models.IntegerField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    start_time = models.DateTimeField(default=datetime.now())
    end_time = models.DateTimeField(default=datetime.now() + timedelta(days=1))


class Bid(models.Model):
    price = models.IntegerField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]


class AuctionPhoto(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='auction_photos/')
