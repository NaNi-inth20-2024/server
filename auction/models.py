from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

from rest_framework.exceptions import ValidationError

MAX_AUCTION_TITLE_LENGTH = 50
MIN_AUCTION_DURATION = timedelta(minutes=1)


class Auction(models.Model):
    title = models.CharField(max_length=MAX_AUCTION_TITLE_LENGTH)
    description = models.TextField()
    initial_price = models.PositiveIntegerField()
    min_bid_price_gap = models.PositiveIntegerField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    start_time = models.DateTimeField(default=datetime.now())
    end_time = models.DateTimeField(default=datetime.now() + timedelta(days=1))

    def clean(self):
        duration = self.start_time - self.end_time
        if duration < MIN_AUCTION_DURATION:
            raise ValidationError("The duration between start and end of auction must be at least 1 hour.")


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
