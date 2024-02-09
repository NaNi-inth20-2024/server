from channels.db import database_sync_to_async

from auction.helpers.models import get_latest_bid_where_auction_id_async
from auction.helpers.validators import auction_validator, bid_validator
from auction.models import Auction, Bid
from auction.serializers import BidSerializer


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

    async def get_bids(self, auction_id, limit, offset):
        bids = await database_sync_to_async(Bid.objects.filter)(auction_id=auction_id)
        bids = await database_sync_to_async(bids.order_by)("-created")
        bids = await database_sync_to_async(lambda: bids[offset : offset + limit])()
        serializer = BidSerializer(bids, many=True)
        return await database_sync_to_async(lambda: serializer.data)()

    async def get_valid_auction(self, id):
        auction = await self.get_auction(id)
        self.auction_validator.is_valid_or_raise(auction)
        return auction

    def get_auction(self, id):
        return database_sync_to_async(Auction.objects.get)(pk=id)

    async def get_winner(self, auction_id):
        auction = await self.get_auction(auction_id)
        self.auction_validator.is_finished_or_raise(auction)
        winner_bid = await database_sync_to_async(
            lambda a_id, won: Bid.objects.filter(auction_id=a_id, won=won).first()
        )(auction.id, True)
        self.bid_validator.is_bid_winner_or_throw(winner_bid)
        return winner_bid


async_auction_service = AsyncAuctionService()
