from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.core.paginator import Paginator

from auction.helpers.models import get_latest_bid_where_auction_id_async
from auction.helpers.pagination import create_paginated_dict
from auction.models import Bid, Auction
from auction.serializers import BidSerializer
from auction.helpers.validators import auction_validator, bid_validator


class AsyncAuctionService:
    auction_validator = auction_validator
    bid_validator = bid_validator

    async def make_bid(self, bid):
        serializer = BidSerializer(data=bid)
        await database_sync_to_async(serializer.is_valid)(raise_exception=True)
        auction = await self.get_valid_auction(bid["auction"])
        bid = await database_sync_to_async(lambda: serializer.validated_data)()
        price = bid["price"]
        self.bid_validator.is_price_more_then_initial(auction, price)

        latest_bid = await get_latest_bid_where_auction_id_async(auction.id, "price")
        latest_price = latest_bid.price if latest_bid else 0
        self.bid_validator.is_price_greater_than_latest(latest_price, price)

        price_gap = price - latest_price
        self.bid_validator.is_great_then_gap_or_raise(auction, price_gap)
        return await database_sync_to_async(serializer.save)()

    async def get_bids(self, auction_id, limit, offset, base_url):
        all_bids = await database_sync_to_async(
            lambda: Bid.objects.filter(auction_id=auction_id).order_by("created"))()
        paginator = Paginator(all_bids, limit)
        page_number = (offset // limit) + 1
        page_obj = await sync_to_async(lambda: paginator.get_page(page_number))()
        ser_bids = await sync_to_async(lambda: BidSerializer(page_obj.object_list, many=True).data)()
        return create_paginated_dict(paginator, page_obj, ser_bids, limit, base_url)

    async def get_valid_auction(self, auction_id):
        auction = await self.get_auction(auction_id)
        self.auction_validator.is_valid_or_raise(auction)
        return auction

    @database_sync_to_async
    def get_auction(self, auction_id):
        return Auction.objects.get(pk=auction_id)

    async def get_winner(self, auction_id):
        auction = await self.get_auction(auction_id)
        self.auction_validator.is_finished_or_raise(auction)
        winner_bid = await database_sync_to_async(
            lambda: Bid.objects
            .filter(auction_id=auction_id, won=True)
            .first()
        )()
        self.bid_validator.is_bid_winner_or_throw(winner_bid)
        return winner_bid


async_auction_service = AsyncAuctionService()
