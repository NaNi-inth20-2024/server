from rest_framework import status
from rest_framework.exceptions import APIException


class BidConflictException(APIException):
    """
    Exception raised when trying to update a bid while the related auction is already started or finished
    """
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Can not create bid. Conflict with current state"


class AuctionFinishedException(APIException):
    """
    Exception raised when trying to update an auction while already being finished
    """
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Auction is already finished"


class AuctionRunningException(APIException):
    """
    Exception raised when trying to update an auction while already being started
    """
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Auction is still running"


class AuctionNotStartedException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Auction is still not started"


class AuctionNotActiveException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Auction is inactive"


class AuctionNotHasWinnerException(APIException):
    status = status.HTTP_404_NOT_FOUND
    default_detail = "Auction has no winner"


class WsAuthException(APIException):
    status = status.HTTP_403_FORBIDDEN
    default_detail = "You are not register"
