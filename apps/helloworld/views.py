import logging

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

logger = logging.getLogger("default")


def hello_world(requests):
    logger.info("hello world")
    return HttpResponse("hello world")
