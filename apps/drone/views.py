import json
import logging

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

# Create your views here.
from rest_framework_yaml.renderers import YAMLRenderer

from apps.drone.droneparse import DroneParse

logger = logging.getLogger("default")


def hello_world(requests):
    logger.info("hello world")
    return HttpResponse("hello world again")


# /usr/local/lib/python3.8/site-packages/rest_framework_yaml/renderers.py

from rest_framework.negotiation import BaseContentNegotiation


class IgnoreClientContentNegotiation(BaseContentNegotiation):
    def select_parser(self, request, parsers):
        """
        Select the first parser in the `.parser_classes` list.
        """
        return parsers[0]

    def select_renderer(self, request, renderers, format_suffix):
        """
        Select the first renderer in the `.renderer_classes` list.
        """
        return (renderers[0], renderers[0].media_type)


class EdroneAPIView(APIView):
    content_negotiation_class = IgnoreClientContentNegotiation

    def post(self, *args, **kwargs):
        logger.info(self.request.data)
        dp = DroneParse(self.request.data)
        drone_yaml = dp.get_yaml()
        logger.info("Get drone yaml")
        logger.info(drone_yaml)
        return HttpResponse(json.dumps({"Data": drone_yaml}))

    get = post
