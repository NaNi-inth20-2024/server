from auction.exceptions import *


class AuctionValidator:
    """
    Validator class for checking the state and validity of auctions.
    """

    def is_lasting(self, auction):
        """
        Checks if the auction is currently in progress (started, not finished, and active).

        :param auction: The Auction object to check.
        :return: True if the auction is currently in progress, False otherwise.
        """

        return auction.started and not auction.finished and auction.active

    def is_lasting_or_raise(self, auction):
        """
        Checks if the auction is in progress, otherwise raises exceptions.

        :param auction: The Auction object to check.
        :raises AuctionNotStartedException: If the auction has not started yet.
        :raises AuctionFinishedException: If the auction has already finished.
        """

        if not auction.started:
            raise AuctionNotStartedException

        if auction.finished:
            raise AuctionFinishedException

    def is_active_or_raise(self, auction):
        """
        Checks if the auction is active, otherwise raises an exception.

        :param auction: The Auction object to check.
        :raises AuctionNotActiveException: If the auction is not active.
        """

        if not auction.active:
            raise AuctionNotActiveException()

    def is_finished_or_raise(self, auction):
        """
        Checks if the auction has finished, otherwise raises an exception.

        :param auction: The Auction object to check.
        :raises AuctionRunningException: If the auction is still running.
        """

        if not auction.finished:
            raise AuctionRunningException()

    def is_not_finished_or_raise(self, auction):
        """
        Checks if the auction has not finished, otherwise raises an exception.

        :param auction: The Auction object to check.
        :raises AuctionFinishedException: If the auction has finished.
        """

        if auction.finished:
            raise AuctionFinishedException()

    def is_valid_or_raise(self, auction):
        """
        Checks if the auction is valid for bidding, otherwise raises exceptions.

        :param auction: The Auction object to check.
        :raises AuctionNotStartedException: If the auction has not started yet.
        :raises AuctionFinishedException: If the auction has already finished.
        :raises AuctionNotActiveException: If the auction is not active.
        """

        self.is_lasting_or_raise(auction)
        self.is_active_or_raise(auction)

    def is_not_started_or_raise(self, auction):
        """
        Checks if the auction has not started yet, otherwise raises exceptions.

        :param auction: The Auction object to check.
        :raises AuctionFinishedException: If the auction has finished.
        :raises AuctionRunningException: If the auction has already started.
        """

        if auction.finished:
            raise AuctionFinishedException()

        if auction.started:
            raise AuctionRunningException()


class BidValidator:
    """
    Validator class for checking the validity of bids in an auction.
    """

    def is_great_then_gap_or_raise(self, auction, price_gap):
        """
        Checks if the price gap of the bid is greater than or equal to the minimum bid price gap of the auction.

        :param auction: The Auction object.
        :param price_gap: The price gap of the bid.
        :raises BidConflictException: If the price gap is too small compared to the minimum bid price gap of the auction.
        """

        if price_gap < auction.min_bid_price_gap:
            raise BidConflictException("Price gap too small")

    def is_price_more_then_initial(self, auction, price):
        """
        Checks if the bid price is greater than the initial price of the auction.

        :param auction: The Auction object.
        :param price: The bid price.
        :raises BidConflictException: If the bid price is less than the initial price of the auction.
        """

        if auction.initial_price > price:
            raise BidConflictException("Initial price of auction greater than bid price")

    def is_price_greater_than_latest(self, latest, curr):
        """
        Checks if the bid price is greater than the latest bid price.

        :param latest: The latest bid price.
        :param curr: The current bid price.
        :raises BidConflictException: If the current bid price is less than or equal to the latest bid price.
        """

        if latest >= curr:
            raise BidConflictException("Price of bid is not greater than the last one")

    def is_bid_winner_or_throw(self, bid):
        """
        Checks if the bid is the winning bid.

        :param bid: The Bid object.
        :raises AuctionNotHasWinnerException: If the auction does not have a winner.
        """

        if bid is None:
            raise AuctionNotHasWinnerException()


auction_validator = AuctionValidator()
bid_validator = BidValidator()
