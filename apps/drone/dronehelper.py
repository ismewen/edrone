import os
from django.conf import settings

from apps.drone.models import Repos


class DroneParse(object):
    DEFAULT_YAML = "./projects/default.yaml"

    def __init__(self, drone_push_params):
        self.drone_push_params = drone_push_params

    @property
    def branch(self):
        return self.drone_push_params.get("build").get("source")

    @property
    def repo_namespace(self):
        return self.drone_push_params.get("repo").get("namespace")

    @property
    def repo_name(self):
        return self.drone_push_params.get("repo").get("name")

    def get_yaml(self):
        yaml_position_directory = str(settings.BASE_DIR) + "/projects/{repo_name}/".format(
            repo_name=self.repo_name,
        )
        if os.path.exists(yaml_position_directory + "{branch_name}.yaml".format(branch_name=self.branch)):
            yaml_file = yaml_position_directory + "{branch_name}.yaml".format(branch_name=self.branch)
        elif os.path.exists(yaml_position_directory + "default.yaml"):
            yaml_file = yaml_position_directory + "default.yaml"
        else:
            yaml_file = self.DEFAULT_YAML
        with open(yaml_file, "r") as f:
            return f.read()


class DroneHelper(object):

    def __init__(self, repo: Repos):
        self.repo = repo

    def create_build(self, params):
        assert "message" in params
        assert "branch" in params
        user = self.repo.user
        build_params = {
            "build_message": params.get("message"),
            "build_source": params.get("branch"),
            "build_trigger": params.get("branch")
        }
        assert ""
