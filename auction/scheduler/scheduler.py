"""
    This module provides functions for managing auction events and WebSocket groups.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone

from auction.consumers import get_group_name
from auction.helpers.models import get_latest_bid_where_auction_id
from auction.models import Auction


def handle_auctions():
    """
    Automatically checks auction instance flags on started and finished auction events.
    This function runs periodically to monitor auction events and take appropriate actions.

    It checks auctions that are scheduled to start or finish based on their start_time and end_time fields.
    If the current time is after the start_time, it marks the auction as started.
    If the current time is after the end_time, it marks the auction as finished, determines the winner bid (if any),
    and closes the associated auction group.

    :return: None
    """
    now = timezone.now()

    # Check auctions scheduled to start
    auctions_to_start = Auction.objects.filter(started=False, finished=False)
    for auction in auctions_to_start:
        if now < auction.start_time:
            continue

        auction.started = True
        auction.save()

    # Check auctions scheduled to finish
    auctions_to_finish = Auction.objects.filter(finished=False, started=True)
    for auction in auctions_to_finish:
        if now < auction.end_time:
            continue

        auction.finished = True
        auction.active = False
        bid = get_latest_bid_where_auction_id(auction.id, "price")
        if bid is not None:
            bid.won = True
            bid.save()

        auction.save()

        async_to_sync(close_auction_group)(auction)


def close_auction_group(auction):
    """
    Closes the WebSocket group associated with a finished auction.

    :param auction: The Auction instance for which the WebSocket group should be closed.
    :return: None
    """
    auction_group_name = get_group_name(auction.id)
    channel_layer = get_channel_layer()
    return channel_layer.group_send(auction_group_name, {"type": "close_channel", "mess": "finish"})


def start():
    """
    Initializes the scheduler and starts monitoring auction events.
    This function sets up the scheduler to execute the handle_auctions function periodically.

    :return: None
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(handle_auctions, IntervalTrigger(seconds=1), name="Start and finish auctions", jobstore="default")
    scheduler.start()
    print("Scheduler started...")
