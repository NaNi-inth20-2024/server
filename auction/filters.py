from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet

from .models import Auction


class AuctionFilter(FilterSet):

    class Meta:
        model = Auction
        fields = {
            "title": ["icontains"],
            "initial_price": ["exact", "lt", "gt"],
            "min_bid_price_gap": ["exact", "lt", "gt"],
            "start_time": [
                "exact",
                "lt",
                "gt",
                "year__lt",
                "month__lt",
                "day__lt",
                "hour__lt",
                "minute__lt",
                "year__gt",
                "month__gt",
                "day__gt",
                "hour__gt",
                "minute__gt",
            ],
            "end_time": [
                "exact",
                "lt",
                "gt",
                "year__lt",
                "month__lt",
                "day__lt",
                "hour__lt",
                "minute__lt",
                "year__gt",
                "month__gt",
                "day__gt",
                "hour__gt",
                "minute__gt",
            ],
        }
