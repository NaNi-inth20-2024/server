from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone

from auction.consumers import get_group_name
from auction.helpers.models import get_latest_bid_where_auction_id
from auction.models import Auction


def handle_auctions():
    now = timezone.now()
    auctions_to_start = Auction.objects.filter(started=False, finished=False)
    for auction in auctions_to_start:
        if now < auction.start_time:
            continue

        auction.started = True
        auction.save()
        print(f"{auction.title} is started")

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
        print(f"Auction \"{auction.title}\" is ended up")


def close_auction_group(auction):
    auction_group_name = get_group_name(auction.id)
    channel_layer = get_channel_layer()
    return channel_layer.group_send(
        auction_group_name,
        {
            "type": "close_channel",
            'mess': "finish"
        }
    )


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(handle_auctions, IntervalTrigger(seconds=1), name="Start and finish auctions", jobstore="default")
    scheduler.start()
    print("Scheduler started...")
