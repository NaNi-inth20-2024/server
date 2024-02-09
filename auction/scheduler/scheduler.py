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
    :return:
    """
    now = timezone.now()
    auctions_to_start = Auction.objects.filter(started=False, finished=False)
    for auction in auctions_to_start:
        if now < auction.start_time:
            continue

        auction.started = True
        auction.save()

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
    auction_group_name = get_group_name(auction.id)
    channel_layer = get_channel_layer()
    return channel_layer.group_send(auction_group_name, {"type": "close_channel", "mess": "finish"})


def start():
    """
    Start the scheduler and wait until an auction has started or finished.
    :return:
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(handle_auctions, IntervalTrigger(seconds=1), name="Start and finish auctions", jobstore="default")
    scheduler.start()
    print("Scheduler started...")
