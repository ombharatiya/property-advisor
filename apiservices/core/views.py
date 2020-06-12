from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from apiservices.core.constants import BLOG


@api_view(["GET"])
def home(request):
    """
    :param request:
    :return: JSON response
    """
    data = {"Success": "Home"}

    return Response(data, status=HTTP_200_OK)


@api_view(["GET"])
def blog(request):
    """
    :param request:
    :return: JSON response
    """

    return Response(BLOG, status=HTTP_200_OK)
