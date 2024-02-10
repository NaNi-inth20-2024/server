from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from auction.models import Bid


def get_latest_bid_where_auction_id(auction_id, field):
    """
    Retrieves the latest bid for a given auction ID based on the specified field.
    :param auction_id: The ID of the auction.
    :param field: The field to use for determining the latest bid (e.g., 'created').
    :return: The latest Bid object or None if no bids are found.
    """
    try:
        return Bid.objects.filter(auction_id=auction_id).latest(field)
    except ObjectDoesNotExist:
        return None


def get_latest_bid_where_auction_id_async(auction_id, field):
    """
    Retrieves the latest bid for a given auction ID based on the specified field.
    :param auction_id: The ID of the auction.
    :param field: The field to use for determining the latest bid (e.g., 'created').
    :return: The latest Bid object or None if no bids are found.
    """
    return database_sync_to_async(get_latest_bid_where_auction_id)(auction_id, field)
