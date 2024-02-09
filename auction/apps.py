"""
Module that contains the config of the application as well as starts scheduler for auctions tracking on ready state.
"""

from django.apps import AppConfig


class AuctionConfig(AppConfig):
    """
    Class that contains the config of the application as well as starts the scheduler for tracking auctions.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "auction"

    def ready(self):
        from auction.scheduler import scheduler

        scheduler.start()
