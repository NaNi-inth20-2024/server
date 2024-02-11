from django.contrib.auth.models import User
from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from auction.filters import AuctionFilter
from auction.helpers.validators import auction_validator, bid_validator
from auction.models import Auction, AuctionPhoto, Bid
from auction.serializers import AuctionPhotoSerializer, AuctionSerializer, BidSerializer
from charityAuctionProject.permissions import IsAuctionAuthorOrReadOnly, IsAuthorOrReadAndCreateOnly


class AuctionViewSet(viewsets.ModelViewSet):
    """
    AuctionViewSet provides AuthenticatedOrReadOnly auction permission while restricting PUT/PATCH for non-authors.
    Auctions cannot be edited while being already started or finished.

    Methods:
        *CRUD*
        activate: Activate auction
        deactivate: Deactivate auction
        get_winner_bid: Get winner of the auction
        get_bids: Get bids of the auction
    """

    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    validator = auction_validator
    bid_validator = bid_validator
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadAndCreateOnly)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = [
        "title",
        "initial_price",
        "min_bid_price_gap",
        "start_time",
        "end_time",
    ]
    search_fields = [
        "title",
    ]
    filterset_class = AuctionFilter

    @extend_schema(
        responses={
            200: AuctionSerializer(),
            409: "Conflict: Trying to update state of the instance while it is already started or finished.",
        },
    )
    @action(detail=True, methods=["PUT"], name="Activate auction")
    def activate(self, request, pk=None):
        auction = self.get_object()
        self.validator.is_not_finished_or_raise(auction)
        auction.active = True
        auction.save()
        return Response(self.get_serializer(auction).data)

    @extend_schema(
        responses={
            200: AuctionSerializer(),
            409: "Conflict: Trying to update state of the instance while it is already started or finished.",
        },
    )
    @action(detail=True, methods=["PUT"], name="Deactivate auction")
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

    @extend_schema(
        responses={
            200: AuctionSerializer(),
            409: "Conflict: Trying to update state of the instance while it is already started or finished.",
        },
    )
    def update(self, request, *args, **kwargs):
        auction = self.get_object()
        self.validator.is_not_started_or_raise(auction)
        super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        auction = self.get_object()
        self.validator.is_not_started_or_raise(auction)
        super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author_username = request.user
        author = User.objects.get(username=author_username)
        serializer.save(author=author)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, url_path="bids", name="get bids by auction id")
    def get_bids(self, request, pk):
        bids = Bid.objects.filter(auction_id=pk).order_by("-created")
        page = self.paginate_queryset(bids)
        if page is not None:
            serializer = BidSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BidSerializer(bids, many=True)
        return Response(serializer.data)


class BidViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows for bid list and view.
    """

    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class AuctionPhotoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows for auction photo list and view.
    """

    queryset = AuctionPhoto.objects.all()
    serializer_class = AuctionPhotoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuctionAuthorOrReadOnly]
