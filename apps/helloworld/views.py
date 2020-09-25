import logging

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.

logger = logging.getLogger("default")


def hello_world(requests):
    logger.info("hello world")
    return HttpResponse("hello world again")


class EdroneAPIView(APIView):
    media_type = 'application/json'

    def post(self, *args, **kwargs):
        logger.info(self.request.data)
        yaml = """
        a: hello
        b: world 
        """
        media_type = 'application/json'
        return HttpResponse(yaml)

    get = post
