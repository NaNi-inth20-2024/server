from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone

MAX_AUCTION_TITLE_LENGTH = 50
MIN_AUCTION_DURATION = timedelta(seconds=10)


def get_auto_end_time():
    return timezone.now() + timedelta(days=1)


class Auction(models.Model):
    title = models.CharField(max_length=MAX_AUCTION_TITLE_LENGTH)
    description = models.TextField()
    initial_price = models.PositiveIntegerField()
    min_bid_price_gap = models.PositiveIntegerField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Bid(models.Model):
    price = models.PositiveIntegerField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]


class AuctionPhoto(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='auction_photos/')
