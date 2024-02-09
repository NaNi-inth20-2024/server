from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from auction.models import Bid


def get_latest_bid_where_auction_id(auction_id, field):
    try:
        return Bid.objects.filter(auction_id=auction_id).latest(field)
    except ObjectDoesNotExist:
        return None


def get_latest_bid_where_auction_id_async(auction_id, field):
    return database_sync_to_async(get_latest_bid_where_auction_id)(auction_id, field)
