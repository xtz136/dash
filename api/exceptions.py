from functools import reduce
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


def api_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        message = str(exc)
        if isinstance(exc.detail, str):
            message = exc.detail
        elif isinstance(exc.detail, dict):
            message = '\n'.join(
                reduce(lambda acc, x: acc + x,
                       exc.detail.values(),
                       []))
        data = {
            'code': response.status_code,
            'message': message,
            'errors': exc.detail}
        response.data = data

    return response
