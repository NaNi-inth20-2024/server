from rest_framework import serializers
from auction.models import Auction, Bid
from django.contrib.auth.models import User


class AuctionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = ['id', 'title', 'description', 'initial_price', 'author']


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'price', "author", "auction"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
