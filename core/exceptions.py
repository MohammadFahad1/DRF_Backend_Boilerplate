import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for Django REST Framework.
    Formats error responses as:
    {
        "success": false,
        "message": "error message",
        "status_code": 400
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        message = ""
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                detail = response.data['detail']
                if isinstance(detail, list):
                    message = " ".join([str(item) for item in detail])
                else:
                    message = str(detail)
            else:
                messages = []
                for field, errors in response.data.items():
                    if isinstance(errors, list):
                        error_str = ", ".join([str(e) for e in errors])
                        messages.append(f"{field}: {error_str}")
                    else:
                        messages.append(f"{field}: {errors}")
                message = "; ".join(messages)
        elif isinstance(response.data, list):
            message = "; ".join([str(item) for item in response.data])
        else:
            message = str(response.data)

        response.data = {
            "success": False,
            "message": message,
            "status_code": response.status_code
        }

    return response
