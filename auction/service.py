from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from auction.exceptions import BidConflictException, AuctionFinishedException, AuctionNotStartedEsception
from auction.models import Auction, Bid


class AuctionService:

    def activate(self, auction):
        self.is_auction_valid_or_raise(auction)
        auction.active = True
        auction.save()

    def deactivate(self, auction):
        self.is_auction_valid_or_raise(auction)
        auction.activate = False
        auction.save()

    def get_winner_bid(self, auction):
        pass

    def is_auction_valid(self, auction):
        return auction.started and not auction.finished and auction.active

    def is_auction_valid_or_raise(self, auction):
        if not auction.started:
            raise AuctionNotStartedEsception

        if auction.finished:
            raise AuctionFinishedException



class BidService:

    def create(self, serializer, auction_id):
        auction = Auction.objects.get(pk=auction_id)
        bid = serializer.validated_data
        price = bid["price"]

        if not auction.active:
            raise AuctionFinishedException()

        if auction.initial_price > price:
            raise BidConflictException("Initial price of auction greater then bid price")

        latest_bid = self.get_latest_bid_where_auction_id(auction_id, 'price')
        latest_price = latest_bid.price if latest_bid else 0

        price_gap = price - latest_price

        if price_gap < auction.min_bid_price_gap:
            raise BidConflictException("Price gap too small")

        serializer.save()

    def get_latest_bid_where_auction_id(self, auction_id, field):
        try:
            return Bid.objects.filter(auction_id=auction_id).latest(field)
        except ObjectDoesNotExist:
            return None


class ScheduleService:

    def start_task(self, time, cb):
        pass
