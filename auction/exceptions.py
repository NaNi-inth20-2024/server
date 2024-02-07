from rest_framework import status
from rest_framework.exceptions import APIException


class BidConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Can not create bid. Conflict with current state'


class AuctionFinishedException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Auction is already closed'


class AuctionRunningException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Auction is still running"


class AuctionNotStartedEsception(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Auction is still not startes"
