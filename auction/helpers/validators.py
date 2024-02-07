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

    def is_valid_or_raise(self, auction):
        self.is_active_or_raise(auction)
        self.is_lasting_or_raise(auction)


class BidValidator:
    def is_great_then_gap_or_raise(self, auction, price_gap):
        if price_gap < auction.min_bid_price_gap:
            raise BidConflictException("Price gap too small")

    def is_price_more_then_initial(self, auction, price):
        if auction.initial_price > price:
            raise BidConflictException("Initial price of auction greater then bid price")


auction_validator = AuctionValidator()
bid_validator = BidValidator()
