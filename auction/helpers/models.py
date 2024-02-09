from django.core.exceptions import ObjectDoesNotExist

from auction.models import Bid


def get_latest_bid_where_auction_id(auction_id, field):
    """
    Returns the latest bid for an auction.
    :param auction_id:
    :param field:
    :return:
    """
    try:
        return Bid.objects.filter(auction_id=auction_id).latest(field)
    except ObjectDoesNotExist:
        return None
