from rest_framework import status
from rest_framework.exceptions import APIException


class BidConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Can not create bid. Conflict with current state"


class AuctionFinishedException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Auction is already finished"


class AuctionRunningException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Auction is still running"


class AuctionNotStartedException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Auction is still not started"


class AuctionNotActiveException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Auction is inactive"
