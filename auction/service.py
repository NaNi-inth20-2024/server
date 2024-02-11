from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.core.paginator import Paginator

from auction.helpers.models import get_latest_bid_where_auction_id_async
from auction.helpers.pagination import create_paginated_dict
from auction.helpers.validators import auction_validator, bid_validator
from auction.models import Auction, Bid
from auction.serializers import BidSerializer
from authentication.service import auth_service
from django.contrib.auth.models import User


class AsyncAuctionService:
    """
    Service class for handling asynchronous operations related to auctions.
    """

    auction_validator = auction_validator
    bid_validator = bid_validator

    async def make_bid(self, bid, author, auction_id):
        """
        Method to make a bid in auction if all assertions is valid.
        :param bid: Dictionary containing bid data.
        :param author: The user making the bid.
        :param auction_id: The ID of the auction for which the bid is made.
        :return: The created bid object.
        :raise: This method can raise various exceptions if bid validation fails.
        """

        serializer = BidSerializer(data=bid)
        await database_sync_to_async(serializer.is_valid)(raise_exception=True)
        auction = await self.get_valid_auction(auction_id)
        bid = await database_sync_to_async(lambda: serializer.validated_data)()
        price = bid["price"]
        self.bid_validator.is_price_more_then_initial(auction, price)

        latest_bid = await get_latest_bid_where_auction_id_async(auction.id, "price")
        latest_price = latest_bid.price if latest_bid else 0
        self.bid_validator.is_price_greater_than_latest(latest_price, price)

        price_gap = price - latest_price
        self.bid_validator.is_great_then_gap_or_raise(auction, price_gap)
        if latest_bid:
            latest_bid.leader = False
            await database_sync_to_async(latest_bid.save)()
        return await database_sync_to_async(serializer.save)(author=author, auction=auction)

    async def get_bids(self, auction_id, limit, offset, base_url):
        """
        Method to get bids asynchronously.
        :param auction_id: The ID of the auction for which bids are retrieved.
        :param limit: The maximum number of bids per page.
        :param offset: The offset for pagination.
        :param base_url: The base URL used for generating next and previous page URLs.
        :return: A dictionary containing paginated bid data.
        """

        all_bids = await database_sync_to_async(
            lambda: Bid.objects.filter(auction_id=auction_id).order_by("-created"))()
        paginator = Paginator(all_bids, limit)
        page_number = (offset // limit) + 1
        page_obj = await sync_to_async(lambda: paginator.get_page(page_number))()
        ser_bids = await sync_to_async(lambda: BidSerializer(page_obj.object_list, many=True).data)()
        return create_paginated_dict(paginator, page_obj, ser_bids, limit, base_url)

    async def get_valid_auction(self, auction_id):
        """
        Method to get a valid auction asynchronously.
        :param auction_id: The ID of the auction to validate.
        :return: The validated auction object.
        :raise: This method can raise an exception if the auction is not valid.
        """

        auction = await self.get_auction(auction_id)
        self.auction_validator.is_valid_or_raise(auction)
        return auction

    @database_sync_to_async
    def get_auction(self, auction_id):
        """
        Method to retrieve an auction asynchronously.
        :param auction_id: The ID of the auction to retrieve.
        :return: The retrieved auction object.
        """

        return Auction.objects.get(pk=auction_id)

    async def get_winner(self, auction_id):
        """
        Method to get the winner of an auction asynchronously.
        :param auction_id: The ID of the auction for which to retrieve the winner.
        :return: The winning bid object.
        :raise: This method can raise an exception if the auction has no winner.
        """

        auction = await self.get_auction(auction_id)
        self.auction_validator.is_finished_or_raise(auction)
        winner_bid = await database_sync_to_async(
            lambda: Bid.objects
            .filter(auction_id=auction_id, won=True)
            .first()
        )()
        self.bid_validator.is_bid_winner_or_throw(winner_bid)
        return winner_bid


class AsyncUserService:
    """
    Service class for handling asynchronous user operations.
    """

    auth_service = auth_service

    @database_sync_to_async
    def get_user(self, headers) -> User:
        """
        Method to retrieve a user asynchronously.
        :param headers: Dictionary containing request headers.
        :return: The retrieved user object.
        """
        return self.auth_service.header_to_user(headers)


async_auction_service = AsyncAuctionService()
async_user_service = AsyncUserService()
