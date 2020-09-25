import logging

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
from rest_framework_yaml.renderers import YAMLRenderer

logger = logging.getLogger("default")

yaml = """
kind: pipeline
name: default

steps:
  - name: docker
    image: plugins/docker
    settings:
      repo: fscripy/edrone
      username:
        from_secret: fscripyu_username
      password:
        from_secret: fscripyu_password
    volumes:
      - name: dockercache
        path: /var/lib/docker
#  - name: deploy
#    image: pelotech/drone-helm3
#    settings:
#      api_server:
#        from_secret: k8s_api_server
#      kubernetes_token:
#        from_secret: k8s_token
#      kube_certificate:
#        from_secret: k8s_ca
#      chart: ./edrone
#      release: edrone
#      helm_command: upgrade
#      wait: true
#      force: true
#      namespace: edrone

  - name: deploy
    image: bitsbeats/drone-helm3
    settings:
      kube_api_server:
        from_secret: k8s_api_server
      kube_token:
        from_secret: k8s_token
      kube_certificate:
        from_secret: k8s_ca
      chart: ./edrone
      release: edrone
      helm_command: upgrade
      wait: true
      force: false
      namespace: default
      vaules_yaml: ["./edrone/values.yaml"]

volumes:
- name: dockercache
  host:
    path: /tmp/docker/${DRONE_REPO}/${DRONE_BRANCH}
"""


def hello_world(requests):
    logger.info("hello world")
    return HttpResponse("hello world again")


class EdroneAPIView(APIView):
    renderer_classes = (YAMLRenderer,)

    def post(self, *args, **kwargs):
        logger.info(self.request.data)
        import json
        return HttpResponse(json.dumps({"data": yaml}))

    get = post
