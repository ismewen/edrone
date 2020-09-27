import logging

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
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
      tag: ${DRONE_COMMIT_SHA}
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
      values: image.tag=${DRONE_COMMIT_SHA}


volumes:
- name: dockercache
  host:
    path: /tmp/docker/${DRONE_REPO}/${DRONE_BRANCH}
"""


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
        data = {
            'build': {'id': 36, 'repo_id': 2, 'trigger': 'ismewen', 'number': 36, 'status': 'pending', 'event': 'push',
                      'action': '', 'link': 'https://github.com/ismewen/edrone/compare/4c6512ca4ebb...ba52a49c188f',
                      'timestamp': 0, 'message': 'sha tag', 'before': '4c6512ca4ebbd9f9e897b15024c15561cd9b5152',
                      'after': 'ba52a49c188f208885119ca6791fddfef802e49e', 'ref': 'refs/heads/master',
                      'source_repo': '',
                      'source': 'master', 'target': 'master', 'author_login': '', 'author_name': 'ismewen',
                      'author_email': 'ismewen@MacBook-Air.local',
                      'author_avatar': 'https://avatars0.githubusercontent.com/u/30500262?v=4', 'sender': 'ismewen',
                      'started': 0, 'finished': 0, 'created': 1601197804, 'updated': 1601197804, 'version': 1},
            'repo': {'id': 2, 'uid': '293063525', 'user_id': 1, 'namespace': 'ismewen', 'name': 'edrone',
                     'slug': 'ismewen/edrone', 'scm': '', 'git_http_url': 'https://github.com/ismewen/edrone.git',
                     'git_ssh_url': 'git@github.com:ismewen/edrone.git', 'link': 'https://github.com/ismewen/edrone',
                     'default_branch': 'master', 'private': False, 'visibility': 'public', 'active': True,
                     'config_path': '.drone.yml', 'trusted': True, 'protected': False, 'ignore_forks': False,
                     'ignore_pull_requests': False, 'timeout': 60, 'counter': 0, 'synced': 0, 'created': 0,
                     'updated': 0,
                     'version': 0}}
        import json
        print("hello world")
        return HttpResponse(json.dumps({"Data": yaml}))

    get = post
