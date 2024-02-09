from rest_framework.routers import DefaultRouter

from auction.views import AuctionViewSet, BidViewSet, AuctionPhotoViewSet

router = DefaultRouter()
router.register(r"auctions", AuctionViewSet, basename="auction")
router.register(r"bids", BidViewSet, basename="bid")
router.register("auctions/images", AuctionPhotoViewSet, basename="auction-image")

urlpatterns = router.urls
