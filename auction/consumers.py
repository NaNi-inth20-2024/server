import json
from json import JSONDecodeError
from urllib.parse import parse_qs

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from rest_framework.exceptions import APIException

from auction.exceptions import WsAuthException
from auction.helpers.exceptions import api_exception_to_json
from auction.models import Auction
from auction.serializers import BidSerializer
from auction.service import async_auction_service, async_user_service
from authentication.service import auth_service

DEFAULT_LIMIT = settings.REST_FRAMEWORK.get("PAGE_SIZE", 10)
AUCTION_GROUP_CLOSE_CODE = 3333


def get_group_name(auction_id):
    return "auction_%s" % auction_id


class AuctionConsumer(AsyncWebsocketConsumer):
    auth_service = auth_service
    auction_service = async_auction_service
    user_service = async_user_service
    auction_group_name = None
    auction_id = None

    async def connect(self):
        try:
            if not await self.get_user():
                raise WsAuthException()
            limit, offset, url = self.parse_parameters()
            await self.auction_service.get_valid_auction(self.auction_id)
            self.auction_group_name = get_group_name(self.auction_id)
            await self.channel_layer.group_add(self.auction_group_name, self.channel_name)
            await self.accept()
            bids = await self.auction_service.get_bids(self.auction_id, limit, offset, url)
            await self.send(text_data=json.dumps(bids))
        except (APIException, Auction.DoesNotExist) as e:
            await self.accept()
            await self.send(text_data=api_exception_to_json(e))
            await self.close()

    def parse_parameters(self):
        self.auction_id = self.scope['url_route']['kwargs']["auction_id"]
        query_params = parse_qs(self.scope['query_string'].decode())
        limit = int(query_params.get('limit', [DEFAULT_LIMIT])[0])
        offset = int(query_params.get('offset', [0])[0])
        url = f"ws:/{self.scope['path']}"
        return limit, offset, url

    async def disconnect(self, close_code):
        if self.auction_group_name is None:
            return
        await self.channel_layer.group_discard(
            self.auction_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        author = await self.get_user()
        if not author:
            await self.close()
            return

        try:
            data = json.loads(text_data)
            bid = await self.auction_service.make_bid(data, author, self.auction_id)
            data = await sync_to_async(lambda: BidSerializer(bid).data)()
            await self.channel_layer.group_send(
                self.auction_group_name, {"type": "send_new_bid", "bid": json.dumps(data)}
            )
        except JSONDecodeError as e:
            await self.send(text_data=json.dumps({"detail": e.msg}))
        except APIException as e:
            await self.send(text_data=api_exception_to_json(e))

    def send_new_bid(self, event):
        bid = event["bid"]
        return self.send(text_data=bid)

    async def close_channel(self, event):
        try:
            winner = await self.auction_service.get_winner(self.auction_id)
            winner = await database_sync_to_async(lambda: BidSerializer(winner).data)()
            await self.send(text_data=json.dumps(winner))
            await self.close(AUCTION_GROUP_CLOSE_CODE)
        except APIException as e:
            await self.send(text_data=api_exception_to_json(e))
