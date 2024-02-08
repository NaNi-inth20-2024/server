from auction.exceptions import *


class AuctionValidator:
    def is_lasting(self, auction):
        return auction.started and not auction.finished and auction.active

    def is_lasting_or_raise(self, auction):
        if not auction.started:
            raise AuctionNotStartedException

        if auction.finished:
            raise AuctionFinishedException

    def is_active_or_raise(self, auction):
        if not auction.active:
            raise AuctionNotActiveException()

    def is_finished_or_raise(self, auction):
        if not auction.finished:
            raise AuctionRunningException()

    def is_not_finished_or_raise(self, auction):
        if auction.finished:
            raise AuctionFinishedException()

    def is_valid_or_raise(self, auction):
        self.is_lasting_or_raise(auction)
        self.is_active_or_raise(auction)

    def is_not_started_or_raise(self, auction):
        if auction.finished:
            raise AuctionFinishedException()

        if auction.started:
            raise AuctionRunningException()


class BidValidator:
    def is_great_then_gap_or_raise(self, auction, price_gap):
        if price_gap < auction.min_bid_price_gap:
            raise BidConflictException("Price gap too small")

    def is_price_more_then_initial(self, auction, price):
        if auction.initial_price > price:
            raise BidConflictException("Initial price of auction greater then bid price")

    def is_price_greater_than_latest(self, latest, curr):
        if latest > curr:
            raise BidConflictException("Price of bid is lesser than last one")


auction_validator = AuctionValidator()
bid_validator = BidValidator()
