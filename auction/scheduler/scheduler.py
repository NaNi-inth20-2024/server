from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.utils import timezone

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
        auction.save()
        print(f"{auction.title} is ended up")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(handle_auctions, IntervalTrigger(seconds=1), name="Start and finish auctions", jobstore="default")
    scheduler.start()
    print("Scheduler started...")
