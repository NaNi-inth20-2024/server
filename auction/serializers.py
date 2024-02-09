from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from auction.models import MIN_AUCTION_DURATION, Auction, Bid, AuctionPhoto
from auction.helpers.validators import auction_validator
from auction.exceptions import AuctionFinishedException, AuctionRunningException

import logging

_logger = logging.getLogger(__name__)


class AuctionSerializer(serializers.ModelSerializer):
    """
    Auction serializer class.
    Validates start and finish time to not be the same.
    """
    class Meta:
        model = Auction
        fields = [
            "id",
            "title",
            "description",
            "initial_price",
            "min_bid_price_gap",
            "author",
            "started",
            "finished",
            "start_time",
            "end_time",
            "active",
        ]
        read_only_fields = ["started", "finished", "id"]

    def validate(self, data):
        """
        Validates start and finish time to not be the same.
        :param data:
        """
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        duration = end_time - start_time
        if duration.total_seconds() < MIN_AUCTION_DURATION.total_seconds():
            raise ValidationError("The duration between start and end of auction must be at least 1 minute.")
        return data

    def update(self, instance, validated_data):
        """
        Updates the instance only for allowed fields.
        :param instance:
        :param validated_data:
        :return:
        """
        allowed_fields = ["title", "description", "initial_price", "min_bid_price_gap", "start_time", "end_time"]
        for field in validated_data:
            if field not in allowed_fields:
                raise serializers.ValidationError(f"Field '{field}' cannot be updated.")

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.initial_price = validated_data.get("initial_price", instance.initial_price)
        instance.min_bid_price_gap = validated_data.get("min_bid_price_gap", instance.min_bid_price_gap)
        instance.start_time = validated_data.get("start_time", instance.start_time)
        instance.end_time = validated_data.get("end_time", instance.end_time)
        instance.active = validated_data.get("active", instance.active)
        instance.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class AuctionPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionPhoto
        fields = '__all__'

    def update(self, instance: AuctionPhoto, validated_data):
        """
        Updates the photo if the related auction is not running or finished.
        :param instance:
        :param validated_data:
        :return:
        :raises AuctionFinishedException: Cannot update photo for a finished auction
        :raises AuctionRunningException: Cannot update photo for a running auction
        """
        auction = instance.auction
        try:
            auction_validator.is_not_started_or_raise(auction)
        except (AuctionFinishedException, AuctionRunningException) as e:
            raise serializers.ValidationError(str(e))
        return super(AuctionPhotoSerializer, self).update(instance, validated_data)

    def save(self, **kwargs):
        """
        Creates the photo if the related auction is not running or finished
        :param kwargs:
        :return:
        :raises AuctionFinishedException: Cannot update photo for a finished auction
        :raises AuctionRunningException: Cannot update photo for a running auction
        """

        try:
            auction = self.validated_data.get("auction")
            auction_validator.is_not_started_or_raise(auction)
        except (AuctionFinishedException, AuctionRunningException) as e:
            raise serializers.ValidationError(str(e))
        super(AuctionPhotoSerializer, self).save(**kwargs)


class BidSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Bid
        fields = ["id", "price", "author", "author_id", "auction", "won", "created"]
        read_only_fields = ["created", "won"]

    def create(self, validated_data):
        author = validated_data.pop('author_id')
        bid = Bid.objects.create(author=author, **validated_data)
        return bid
