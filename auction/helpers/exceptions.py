from rest_framework import status
from rest_framework.exceptions import APIException
from rich import json


def api_exception_to_json(e):
    if isinstance(e, APIException):
        error = {
            "detail": e.detail,
            "status_code": e.status_code,
        }
    else:
        error = {"detail": e.__str__()}

    return json.dumps(error)
