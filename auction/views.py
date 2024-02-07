from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from auction import serializers
from auction.helpers.models import get_latest_bid_where_auction_id
from auction.models import Bid, Auction
from auction.helpers.validators import auction_validator, bid_validator


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = serializers.AuctionSerializer
    validator = auction_validator

    @action(detail=True, name="Activate auction")
    def activate(self, request, pk=None):
        auction = self.get_object()
        self.validator.is_lasting_or_raise(auction)
        auction.active = True
        auction.save()
        return Response(self.get_serializer(auction).data)

    @action(detail=True, name="Deactivate auction")
    def deactivate(self, request, pk=None):
        auction = self.get_object()
        self.validator.is_lasting_or_raise(auction)
        auction.active = False
        auction.save()
        return Response(self.get_serializer(auction).data)

    @action(detail=True, name="Winner bid of auction")
    def winner_bid(self, request, pk=None):
        auction = self.get_object()
        serializer = self.service.get_winner_bid(auction)
        return Response(
            serializer,
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        pass


class BidViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = serializers.BidSerializer
    validator = bid_validator
    auction_validator = auction_validator

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auction_id = request.data["auction"]
        auction = Auction.objects.get(pk=auction_id)
        self.auction_validator.is_active_or_raise(auction)

        bid = serializer.validated_data
        price = bid["price"]
        self.validator.is_price_more_then_initial(auction, price)

        latest_bid = get_latest_bid_where_auction_id(auction_id, 'price')
        latest_price = latest_bid.price if latest_bid else 0

        price_gap = price - latest_price
        self.validator.is_great_then_gap_or_raise(auction, price_gap)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, url_path="auction")
    def get_bids_by_auction_id(self, request, pk):
        bids = Bid.objects.filter(auction_id=pk)
        page = self.paginate_queryset(bids)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(bids, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
