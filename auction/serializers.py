import logging

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from auction.exceptions import AuctionFinishedException, AuctionRunningException
from auction.helpers.validators import auction_validator
from auction.models import MIN_AUCTION_DURATION, Auction, AuctionPhoto, Bid

_logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class AuctionPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionPhoto
        fields = "__all__"

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


class AuctionSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        images = AuctionPhoto.objects.filter(auction=obj)
        return AuctionPhotoSerializer(images, many=True, read_only=True).data

    class Meta:
        model = Auction
        fields = [
            "id",
            "title",
            "description",
            "initial_price",
            "min_bid_price_gap",
            "images",
            "author",
            "started",
            "finished",
            "start_time",
            "end_time",
            "active",
        ]
        read_only_fields = ["started", "finished", "id", "author", "images",]

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

    def create(self, validated_data):
        """
        Method to create auction instance with id from author model
        :param validated_data:
        :return:
        """
        author = validated_data.pop("author")
        bid = Auction.objects.create(author=author, **validated_data)
        return bid


class BidSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    auction = AuctionSerializer(many=False, read_only=True)

    class Meta:
        model = Bid
        fields = ["id", "price", "author", "auction", "won", "created", "leader"]
        read_only_fields = ["created", "won", "leader"]

    def create(self, validated_data):
        """
        Method to create bid instance with ids from author and auction models
        :param validated_data:
        :return:
        """
        author = validated_data.pop("author")
        auction = validated_data.pop("auction")
        bid = Bid.objects.create(author=author, auction=auction, **validated_data)
        return bid
