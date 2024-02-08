from rest_framework.routers import DefaultRouter

from auction.views import AuctionViewSet, BidViewSet

router = DefaultRouter()
router.register(r"auctions", AuctionViewSet, basename="auction")
router.register(r"bids", BidViewSet, basename="bid")

urlpatterns = router.urls
