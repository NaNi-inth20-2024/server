from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from auction.helpers.models import get_latest_bid_where_auction_id
from auction.helpers.validators import auction_validator, bid_validator
from auction.models import Auction, Bid
from auction.serializers import AuctionSerializer, BidSerializer, UserSerializer


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    validator = auction_validator
    bid_validator = bid_validator
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(detail=True, name="Activate auction")
    def activate(self, request, pk=None):
        auction = self.get_object()
        self.validator.is_not_finished_or_raise(auction)
        auction.active = True
        auction.save()
        return Response(self.get_serializer(auction).data)

    @action(detail=True, name="Deactivate auction" "")
    def deactivate(self, request, pk=None):
        auction = self.get_object()
        self.validator.is_not_finished_or_raise(auction)
        auction.active = False
        auction.save()
        return Response(self.get_serializer(auction).data)

    @action(detail=True, name="Winner bid of auction", url_path="winner")
    def get_winner_bid(self, request, pk=None):
        auction = self.get_object()
        self.validator.is_finished_or_raise(auction)
        winner_bid = Bid.objects.filter(auction_id=auction.id, won=True).first()
        self.bid_validator.is_bid_winner_or_throw(winner_bid)
        serializer = BidSerializer(winner_bid)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        self.validator.is_not_started_or_raise()
        self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.validator.is_not_started_or_raise()
        self.destroy(request, *args, **kwargs)

    @action(detail=True, url_path="bids", name="get bids by auction id")
    def get_bids(self, request, pk):
        bids = Bid.objects.filter(auction_id=pk).order_by('-created')
        page = self.paginate_queryset(bids)
        if page is not None:
            serializer = BidSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)


class BidViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
