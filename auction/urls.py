from rest_framework.routers import DefaultRouter

from auction.views import AuctionViewSet, BidViewSet, UserViewSet

router = DefaultRouter()
router.register(r"auctions", AuctionViewSet, basename="auction")
router.register(r"bids", BidViewSet, basename="bid")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = router.urls
