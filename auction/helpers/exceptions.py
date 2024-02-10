from rest_framework.exceptions import APIException
from rich import json


def api_exception_to_json(e):
    """
       Returns a JSON representation of an API exception or the name of any other exception as JSON.
       :param e: An ApiException object or any other exception.
       :return: JSON representation of the exception.
    """
    if isinstance(e, APIException):
        error = {
            "detail": e.detail,
            "status_code": e.status_code,
        }
    else:
        error = {"detail": e.__str__()}

    return json.dumps(error)
