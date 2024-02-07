from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from auction import serializers
from auction.models import Bid, Auction
from auction.service import BidService, AuctionService


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = serializers.AuctionSerializer
    auction_service = AuctionService()

    @action(detail=True, name="Activate auction")
    def activate(self, request, pk=None):
        auction = self.get_object()
        self.auction_service.activate(auction)
        return Response(
            self.get_serializer(auction).data,
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=True, name="Deactivate auction")
    def deactivate(self, request, pk=None):
        auction = self.get_object()
        self.auction_service.deactivate(auction)
        return Response(
            self.get_serializer(auction).data,
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=True, name="Winner bid of auction")
    def winner_bid(self, request, pk=None):
        auction = self.get_object()
        winner_bid = self.auction_service.get_winner_bid(auction)
        return Response(
            winner_bid,
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        pass


class BidViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = serializers.BidSerializer
    bidService = BidService()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auction_id = request.data["auction"]
        self.bidService.create(serializer, auction_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self):
        pass


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
