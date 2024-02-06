from django.urls import path, include
from rest_framework.routers import DefaultRouter
from auction import views

router = DefaultRouter()
router.register(r'auctions', views.AuctionViewSet, basename='auction')
router.register(r'bids', views.BidViewSet, basename='bid')
router.register(r'users', views.UserViewSet, basename='user')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

