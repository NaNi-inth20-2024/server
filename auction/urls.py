from django.urls import include, path
from rest_framework.routers import DefaultRouter

from auction.views import AuctionPhotoViewSet, AuctionViewSet, BidViewSet

router = DefaultRouter()
router.register(r"auctions", AuctionViewSet, basename="auction")
router.register(r"bids", BidViewSet, basename="bid")
router.register("auction-photos", AuctionPhotoViewSet, basename="auction-image")

urlpatterns = [
    path("", include(router.urls)),
]
