import json
import logging

from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.views import APIView

from apps.drone import serializers
from apps.drone.dronehelper import DroneParse
from apps.drone.models import Repos, Builds

from cdrone.core import APIViewSet, router
from cdrone.negotiation import IgnoreClientContentNegotiation

logger = logging.getLogger("default")


class EdroneAPIView(APIView):
    content_negotiation_class = IgnoreClientContentNegotiation

    def post(self, *args, **kwargs):
        logger.info(self.request.data)
        dp = DroneParse(self.request.data)
        drone_yaml = dp.get_yaml()
        logger.info("Get drone yaml")
        logger.info(drone_yaml)
        logger.info(self.request.headers)
        return HttpResponse(json.dumps({"Data": drone_yaml}))

    get = post


class BuildAPIViewSet(APIViewSet):
    custom_name = "build"
    path = "builds"

    model = Builds
    serializer_class = serializers.BuildSerializer

    serializer_mapping = {
        "create": serializers.BuildCreateSerializer
    }


class RepoAPIViewSet(APIViewSet):
    custom_name = "repo"
    path = "repos"

    nested_viewsets = [BuildAPIViewSet]

    model = Repos
    serializer_class = serializers.RepoSerializer


router.custom_register(RepoAPIViewSet)
